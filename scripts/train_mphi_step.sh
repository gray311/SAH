#!/usr/bin/env bash
# Train phi on one outer step's GRPO group, then merge for serving.
#   bash scripts/train_mphi_step.sh <round_dir> <step_tag> [prev_ckpt_dir]
# e.g. bash scripts/train_mphi_step.sh $RUN_ROOT/self_adapt_harness/outer/round001 s001
#      bash scripts/train_mphi_step.sh .../round002 s002 $MODEL_ROOT/checkpoints/self_adapt_harness/mphi_s001
#
# Chain: grpo_to_replay (login node, pure python) -> Weave train_qwen35_lora.slurm
# (slime offline GRPO, LoRA r64/a128 on 4 GPUs) -> merge.slurm (afterok) ->
# merged HF ckpt at $MODEL_ROOT/exports/self_adapt_harness/mphi_<step>.
# Only phi trains; M0 is never touched (plan.md §0).
set -euo pipefail
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh

ROUND_DIR="${1:?usage: train_mphi_step.sh <round_dir> <step_tag> [prev_ckpt]}"
STEP="${2:?step tag, e.g. s001}"
PREV_CKPT="${3:-}"

sbatch_retry() {  # transient slurmctld failures are common under load
  local out
  for _ in $(seq 1 30); do
    if out=$("$@" 2>&1); then echo "$out" | tail -1; return 0; fi
    echo "  (sbatch failed: $(echo "$out" | tail -1); retrying in 60s)" >&2
    sleep 60
  done
  echo "sbatch failed after 30 attempts" >&2; return 1
}

W="$CODE_ROOT/Weave_v2"
SAH="$CODE_ROOT/self_adapt_harness"
BASE_HF="$MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a"
SAVE_CKPT="$MODEL_ROOT/checkpoints/self_adapt_harness/mphi_$STEP"
MERGED="$MODEL_ROOT/exports/self_adapt_harness/mphi_$STEP"
REPLAY="$ROUND_DIR/replay.jsonl"

echo "[1/3] convert grpo_batch -> slime replay"
python3 "$SAH/src/training/grpo_to_replay.py" --rounds "$ROUND_DIR" --out "$REPLAY"
N_ROWS=$(wc -l < "$REPLAY")
[ "$N_ROWS" -ge 2 ] || { echo "only $N_ROWS trainable rows — no gradient signal; aborting"; exit 1; }

echo "[2/3] submit GRPO training ($N_ROWS rows, LoRA r64/a128, lr 6e-5, 3 epochs)"
mkdir -p "$SAVE_CKPT" "$LOG_ROOT/slurm"
TRAIN_ENV=(RUN_SCRIPT="$W/scripts/train/run_qwen35_grpo_offline_lora.sh"
           PROMPT_DATA="$REPLAY" SAVE_CKPT="$SAVE_CKPT" HF_CKPT="$BASE_HF"
           LR=6e-5 LORA_RANK=64 LORA_ALPHA=128 NUM_GPUS=4 NUM_EPOCH=3
           ROLLOUT_BATCH_SIZE="$N_ROWS" GLOBAL_BATCH_SIZE=8 MICRO_BATCH_SIZE=1
           LOG_PROBS_CHUNK_SIZE=2048)
[ -n "$PREV_CKPT" ] && TRAIN_ENV+=(LOAD_CKPT="$PREV_CKPT" LORA_RESUME=1)
TRAIN_JOB=$(cd "$W" && sbatch_retry env "${TRAIN_ENV[@]}" sbatch --parsable scripts/train/train_qwen35_lora.slurm)
echo "  train job: $TRAIN_JOB"

echo "[3/3] submit merge (afterok:$TRAIN_JOB)"
MERGE_JOB=$(cd "$W" && sbatch_retry env MERGE_SCRIPT="$W/scripts/merge/merge_in_container.sh" \
  HF_CKPT="$BASE_HF" CKPT_DIR="$SAVE_CKPT" OUT="$MERGED" \
  sbatch --parsable --dependency=afterok:"$TRAIN_JOB" scripts/merge/merge.slurm)
echo "  merge job: $MERGE_JOB"
echo
echo "merged M_phi -> $MERGED"
echo "next step example:"
echo "  ROUND_ID=<r+1> TASKS=<next_task> BASES_FILE=$ROUND_DIR/next_bases.json \\"
echo "  MPHI_PATH=$MERGED sbatch $SAH/scripts/outer_round.sbatch"