#!/usr/bin/env bash
# Run the incoming parent H2 under cand01's exact historical rollout contract.

set -euo pipefail
umask 027
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh

readonly RUN_DIR="$RUN_ROOT/campaigns/debug-evolve-qwen35-6186121"
readonly SNAPSHOT_DIR="$RUN_DIR/source_snapshot"
readonly ROUND_DIR="$RUN_DIR/rounds/round001"
readonly INSPECTION_DIR="$RUN_DIR/inspection/ac2_round001"
readonly PHASE_DIR="$INSPECTION_DIR/paired_replay_cand01"
readonly TASK_ID="eft__math__second_autocorr_ineq"
readonly PARENT_H2="$SNAPSHOT_DIR/src/inner/harness"
readonly DECODE_SEED=200001

source "$RUN_DIR/launchers/iad_vllm_server_common.sh"
if [ -s "$PHASE_DIR/PASSED" ]; then
  echo "paired replay already passed: $PHASE_DIR"
  exit 0
fi
mkdir -p "$PHASE_DIR/control" "$PHASE_DIR/server_protocol"
printf 'started_utc=%s\njob_id=%s\ndecode_seed=%s\n' \
  "$(date -Is -u)" "$SLURM_JOB_ID" "$DECODE_SEED" > "$PHASE_DIR/STARTED"

cleanup() {
  local rc=$?
  trap - EXIT INT TERM
  stop_vllm_server
  if [ "$rc" -ne 0 ] && [ ! -s "$PHASE_DIR/PASSED" ]; then
    printf 'failed_utc=%s\nreturncode=%s\n' \
      "$(date -Is -u)" "$rc" > "$PHASE_DIR/FAILED"
  fi
  exit "$rc"
}
trap cleanup EXIT INT TERM

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$SNAPSHOT_DIR/src:$SNAPSHOT_DIR"
export SAH_TASK_TEXT_REGISTRY="$SNAPSHOT_DIR/provenance/task_text_registry.json"
export SAH_TASK_TEXT_ENFORCE=1
export OPENAI_API_KEY=EMPTY

nvidia-smi -L > "$PHASE_DIR/nvidia-smi-L.txt"
nvidia-smi --query-gpu=name,uuid,driver_version,memory.total,compute_cap \
  --format=csv,noheader > "$PHASE_DIR/gpu.csv"
start_vllm_server "$PHASE_DIR" 8800 131072

cd "$SNAPSHOT_DIR/src"
timeout --foreground --kill-after=60s 2400s \
  "$SAH_PYTHON" -m inner.run_baseline \
    --harness-dir "$PARENT_H2" \
    --ids "$TASK_ID" \
    --base-url http://127.0.0.1:8800/v1 \
    --model "$SAH_SERVED_MODEL" \
    --max-evals 2 \
    --eval-timeout 180 \
    --llm-timeout 600 \
    --seed "$DECODE_SEED" \
    --seed-programs-file "$ROUND_DIR/seed_programs_in.json" \
    --eval-python "$SAH_PYTHON" \
    --require-trajectory \
    --out "$PHASE_DIR/control" \
    > "$PHASE_DIR/control.log" 2>&1

"$SAH_PYTHON" "$INSPECTION_DIR/paired_replay_cand01_audit.py" \
  --run-dir "$RUN_DIR" --control-dir "$PHASE_DIR/control" \
  --out "$PHASE_DIR/paired_effect.json" \
  2>&1 | tee "$PHASE_DIR/audit.log"
printf 'passed_utc=%s\n' "$(date -Is -u)" > "$PHASE_DIR/PASSED"
echo "paired replay passed: $PHASE_DIR"
