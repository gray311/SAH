#!/usr/bin/env bash
# Runs INSIDE the aarch64 container (launched by outer_round.sbatch).
# One full outer round:
#   1. deps + serve N vLLM replicas of the frozen base checkpoint
#      (M0 executor; M_phi proposer = same weights in round 1 / merged phi later)
#   2. propose: M_phi + H1 -> K candidate H2 packages (outer.outer_round propose)
#   3. rollouts: for each valid candidate, one process runs the inner loop over
#      the round's task list (<=MAX_EVALS evals/task), sharded across replicas
#   4. collect: rewards + GRPO advantages -> grpo_batch.jsonl
# Env in: OUT_DIR ROUND_ID K N_REPLICAS MAX_EVALS EVAL_TIMEOUT MODEL_PATH
#         SERVED_MODEL VLLM_ENV REPO BASE_HARNESS PROPOSER_SEED
set -euo pipefail
umask 027
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
log(){ echo "[$(date -Is)] $*"; }

ROUND_DIR="$OUT_DIR/round$(printf '%03d' "$ROUND_ID")"
mkdir -p "$ROUND_DIR"

# --- deps --- #
export UV_BREAK_SYSTEM_PACKAGES=1
log "installing deps"
uv pip install --system -e "$CODE_ROOT/NexAU" jax optax orjson cvxpy > "$OUT_DIR/pip.log" 2>&1 \
  || { tail -30 "$OUT_DIR/pip.log"; exit 1; }
python3 -c "from nexau import Agent; import jax, optax, orjson, cvxpy, openai; print('deps OK')"

# --- serve N replicas --- #
# Split serving (plan.md §0/§6.3): when MPHI_PATH is set (step >= 2, trained
# phi), replica 0 serves the merged M_phi (PROPOSE ONLY) and replicas 1..N-1
# serve the frozen base M0 (INNER LOOP ONLY) — the executor stays bit-frozen.
# Step 1 (phi == 0): every replica serves the base and both roles share them.
export VLLM_USE_FLASHINFER_SAMPLER=0
declare -a VPIDS=()
for g in $(seq 0 $((N_REPLICAS - 1))); do
  port=$((8800 + g))
  ckpt="$MODEL_PATH"
  if [ -n "${MPHI_PATH:-}" ] && [ "$g" -eq 0 ]; then ckpt="$MPHI_PATH"; fi
  log "replica $g serves: $ckpt"
  CUDA_VISIBLE_DEVICES=$g "$VLLM_ENV/bin/python" "$VLLM_ENV/bin/vllm" serve "$ckpt" \
    --host 0.0.0.0 --port "$port" --served-model-name "$SERVED_MODEL" \
    --max-model-len 131072 --max-num-seqs 8 --max-num-batched-tokens 16384 \
    --gpu-memory-utilization 0.90 --enforce-eager --language-model-only \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml \
    > "$OUT_DIR/vllm-$g.log" 2>&1 &
  VPIDS+=($!)
done
trap 'for p in "${VPIDS[@]:-}"; do kill -KILL "$p" 2>/dev/null || true; done' EXIT
for g in $(seq 0 $((N_REPLICAS - 1))); do
  port=$((8800 + g)); ok=0
  for _ in $(seq 1 240); do
    curl -sf "http://127.0.0.1:$port/v1/models" >/dev/null 2>&1 && { ok=1; break; }
    kill -0 "${VPIDS[$g]}" 2>/dev/null || { log "replica $g died"; tail -40 "$OUT_DIR/vllm-$g.log"; exit 1; }
    sleep 5
  done
  [ "$ok" = 1 ] || { log "replica $g not ready"; exit 1; }
  log "replica $g ready (:$port)"
done

cd "$REPO/src"
export OPENAI_API_KEY=EMPTY

# --- propose (instance-wise: K candidates per task) --- #
# With split serving, propose targets ONLY replica 0 (M_phi); otherwise all.
PROPOSE_REPLICAS="$N_REPLICAS"
[ -n "${MPHI_PATH:-}" ] && PROPOSE_REPLICAS=1
log "propose: task(s) [$TASKS], K=$K, H1-agent runs across $PROPOSE_REPLICAS replica(s)"
python3 -m outer.outer_round propose \
  --round-dir "$ROUND_DIR" --round "$ROUND_ID" --k "$K" \
  --tasks $TASKS \
  ${BASES_FILE:+--bases-file "$BASES_FILE"} \
  --n-replicas "$PROPOSE_REPLICAS" --model "$SERVED_MODEL" \
  --max-evals "$MAX_EVALS" ${PROPOSER_SEED:+--seed "$PROPOSER_SEED"} \
  --parallel "${PROPOSE_PAR:-8}" \
  2>&1 | tee "$ROUND_DIR/propose.log"

# --- rollouts: one process per (task, valid candidate), bounded pool --- #
mapfile -t PAIRS < <(python3 - "$ROUND_DIR" <<'PY'
import json, sys
meta = json.load(open(f"{sys.argv[1]}/round.json"))
for tid in meta["tasks_order"]:
    for c in meta["per_task"][tid]["candidates"]:
        if c["valid"]:
            print(f"{tid}:{c['k']}")
PY
)
MAX_PAR="${ROLLOUT_PAR:-8}"
log "rollouts: ${#PAIRS[@]} (task,cand) pairs, <= $MAX_PAR concurrent"
mkdir -p "$ROUND_DIR/rollout_logs"
# With split serving, M_phi (replica 0) is no longer needed after propose:
# restart replica 0 with the FROZEN BASE so rollouts get all N replicas
# (audit finding: replica 0 idled for the entire ~3.7h rollout phase).
if [ -n "${MPHI_PATH:-}" ]; then
  log "propose done — restarting replica 0 with frozen base for rollouts"
  kill -KILL "${VPIDS[0]}" 2>/dev/null || true; wait "${VPIDS[0]}" 2>/dev/null || true
  CUDA_VISIBLE_DEVICES=0 "$VLLM_ENV/bin/python" "$VLLM_ENV/bin/vllm" serve "$MODEL_PATH" \
    --host 0.0.0.0 --port 8800 --served-model-name "$SERVED_MODEL" \
    --max-model-len 131072 --max-num-seqs 8 --max-num-batched-tokens 16384 \
    --gpu-memory-utilization 0.90 --enforce-eager --language-model-only \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml \
    > "$OUT_DIR/vllm-0-rollout.log" 2>&1 &
  VPIDS[0]=$!
  for _ in $(seq 1 240); do
    curl -sf "http://127.0.0.1:8800/v1/models" >/dev/null 2>&1 && { log "replica 0 (frozen base) ready"; break; }
    kill -0 "${VPIDS[0]}" 2>/dev/null || { log "replica 0 restart died"; break; }
    sleep 5
  done
fi
# Rollouts (frozen M0) now use ALL replicas in both modes.
RB=8800; RN="$N_REPLICAS"
idx=0; rc=0
for pair in "${PAIRS[@]:-}"; do
  [ -n "$pair" ] || continue
  tid="${pair%%:*}"; k="${pair##*:}"
  port=$((RB + idx % RN)); idx=$((idx + 1))
  cdir=$(printf '%s/tasks/%s/cand%02d' "$ROUND_DIR" "$tid" "$k")
  while (( $(jobs -rp | wc -l) >= MAX_PAR )); do wait -n || rc=1; done
  OPENAI_BASE_URL="http://127.0.0.1:$port/v1" python3 -m inner.run_baseline \
    --harness-dir "$cdir" --ids "$tid" \
    --base-url "http://127.0.0.1:$port/v1" --model "$SERVED_MODEL" \
    --max-evals "$MAX_EVALS" ${EVAL_TIMEOUT:+--eval-timeout "$EVAL_TIMEOUT"} \
    --eval-python python3 --no-trajectory \
    --out "$ROUND_DIR/rollouts/$tid/cand$(printf '%02d' "$k")" \
    > "$ROUND_DIR/rollout_logs/${tid}-cand$(printf '%02d' "$k").log" 2>&1 &
done
while (( $(jobs -rp | wc -l) > 0 )); do wait -n || rc=1; done
log "rollouts finished (rc=$rc)"

# --- collect --- #
python3 -m outer.outer_round collect --round-dir "$ROUND_DIR" 2>&1 | tee "$ROUND_DIR/collect.log"
log "round $ROUND_ID done -> $ROUND_DIR"
