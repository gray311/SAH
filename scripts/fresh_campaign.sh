#!/usr/bin/env bash
# Single-task fresh campaign from BASE phi, generative genome (h2spec/1.0).
#   fresh_campaign.sh <task_id> <n_steps> <round_base> [force_tool_frac]
# Round r: propose (M_phi = latest merged phi, or BASE for step 1) with the
# generative genome -> rollout -> collect -> GRPO train next phi from prev ckpt
# -> merge -> repeat. Inheritance/feedback live in a task-local workspace so the
# main campaign is untouched. RL budget = n_steps (reset from scratch).
set -uo pipefail
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
TASK="$1"; NSTEPS="$2"; RBASE="$3"; FTF="${4:-0.25}"; WS="${5:-$RUN_ROOT/self_adapt_harness/fresh_cp}"
SAH="$CODE_ROOT/self_adapt_harness"
OUT="$RUN_ROOT/self_adapt_harness/outer"
BASE_PHI="$MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a"
TAG=$(echo "$TASK" | sed 's/.*__//; s/_//g' | cut -c1-8)   # short per-task checkpoint tag
log(){ echo "[$(date -Is)] [fresh:${TASK##*__}] $*"; }

bases="$WS/round000_bases.json"
prev_ckpt=""                       # empty => train from base on step 1
phi="$BASE_PHI"                    # step 1 proposer = base

for i in $(seq 0 $((NSTEPS - 1))); do
  [ -f "$WS/STOP" ] && { log "STOP flag — exiting"; break; }
  R=$((RBASE + i)); RD="$OUT/round$(printf '%03d' "$R")"
  STAG=$(printf "f_%s_%02d" "$TAG" "$i")
  log "step $((i+1))/$NSTEPS: round$R propose (phi=$(basename "$phi")) ftf=$FTF"

  JOB=""
  for _ in $(seq 1 30); do
    RAW=$(cd "$SAH" && env ROUND_ID="$R" TASKS="$TASK" K="${K:-8}" MAX_EVALS="${MAX_EVALS:-20}" \
      FORCE_TOOL_FRAC="$FTF" \
      BASES_FILE="$bases" MPHI_PATH="$phi" \
      SEED_PROGRAMS_FILE="$WS/best_programs.json" \
      FEEDBACK_FILE="$WS/task_feedback.json" \
      sbatch --parsable scripts/outer_round.sbatch 2>&1)
    JOB=$(echo "$RAW" | grep -oE '[0-9]{6,}' | tail -1)
    [ -n "$JOB" ] && break; sleep 60
  done
  [ -n "$JOB" ] || { log "submit failed"; break; }
  log "  job $JOB"
  while squeue -j "$JOB" -h -o '%T' 2>/dev/null | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do sleep 150; done

  if [ ! -f "$RD/grpo_batch.jsonl" ] && [ -f "$RD/round.json" ]; then
    (cd "$SAH/src" && python3 -m outer.outer_round collect --round-dir "$RD") >/dev/null 2>&1
  fi
  [ -f "$RD/round_summary.json" ] || { log "no summary — stop"; break; }
  python3 "$SAH/scripts/sanitize_grpo_batch.py" "$RD" >/dev/null 2>&1
  # sync inheritance + feedback into the task-local workspace
  [ -f "$OUT/best_programs.json" ] && cp "$OUT/best_programs.json" "$WS/best_programs.json" 2>/dev/null || true
  [ -f "$OUT/task_feedback.json" ] && cp "$OUT/task_feedback.json" "$WS/task_feedback.json" 2>/dev/null || true
  SUM=$(python3 -c "
import json
g=json.load(open('$RD/round_summary.json'))['groups']['$TASK']
print('base=%.5g best=%s improved=%s'%(g['base_score'], g['best_score'], g['improved']))")
  DIMS=$(python3 -c "
import json
d=json.load(open('$RD/round.json'))
from collections import Counter
cnt=Counter()
for c in d['per_task']['$TASK']['candidates']:
    for f in c.get('changed_fields',[]):
        if f.startswith('new_'): cnt[f.split('.')[0]]+=1
print(dict(cnt))")
  log "  $SUM | gen_dims=$DIMS"
  bases="$RD/next_bases.json"

  # ---- GRPO train next phi ----
  V=$(python3 -c "import json;d=json.load(open('$RD/round.json'));print(sum(1 for c in d['per_task']['$TASK']['candidates'] if c['valid']))")
  if [ "$V" -ge 4 ]; then
    cd "$SAH"
    if [ -z "$prev_ckpt" ]; then
      KL_COEF=0.05 NUM_EPOCH=3 bash scripts/train_mphi_step.sh "$RD" "$STAG" > /tmp/fcp_train.txt 2>&1
    else
      KL_COEF=0.05 NUM_EPOCH=3 bash scripts/train_mphi_step.sh "$RD" "$STAG" "$prev_ckpt" > /tmp/fcp_train.txt 2>&1
    fi
    T=$(grep -oP 'train job: \K[0-9]+' /tmp/fcp_train.txt); M=$(grep -oP 'merge job: \K[0-9]+' /tmp/fcp_train.txt)
    if [ -n "$T" ]; then
      while squeue -j "$T" -h -o '%T' 2>/dev/null | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do sleep 120; done
      if [ "$(sacct -j "$T" -X -n -o State|head -1|xargs)" = "COMPLETED" ]; then
        while squeue -j "$M" -h -o '%T' 2>/dev/null | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do sleep 60; done
        MERGED="$MODEL_ROOT/exports/self_adapt_harness/mphi_$STAG"
        if ls "$MERGED"/*.safetensors >/dev/null 2>&1; then
          phi="$MERGED"; prev_ckpt="$MODEL_ROOT/checkpoints/self_adapt_harness/mphi_$STAG"
          log "  trained -> mphi_$STAG"
        fi
      fi
    fi
  else
    log "  degenerate group (V=$V) — skip training, keep phi"
  fi
done
log "fresh campaign done"
