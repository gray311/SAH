#!/usr/bin/env bash
# One outer-loop STEP (one task) on a GB200 node — the online GRPO cadence:
#   task tau: M_phi + H1(tau) -> K=8 candidate H2 -> M0 + each H2 -> 8 rollouts
#   on tau (<=20 evals each) -> 8 rewards (one GRPO group) -> grpo_batch.jsonl.
#   Then: train phi on this group (src/training), merge, and launch the next
#   step (next task / same task) against the updated M_phi.
#
# Submit:
#   source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
#   mkdir -p "$LOG_ROOT/slurm"
#   ROUND_ID=1 TASKS=eft__math__circle_packing sbatch scripts/outer_round.sbatch
# Env knobs: ROUND_ID TASKS K MAX_EVALS EVAL_TIMEOUT BASES_FILE MODEL_PATH
#   PROPOSER_SEED OUT_TAG ROLLOUT_PAR PROPOSE_PAR PROTOCOL
#   TASKS:        the task for this step (space-separated list allowed, default CP).
#   BASES_FILE:   per-task current-best-H2 registry (default: initial H2 + static
#                 baseline). For round r>1 use the previous round's next_bases.json.
#   MODEL_PATH:   serving checkpoint. Round 1 = frozen base (M_phi==M0 weights).
#                 After GRPO, point at the merged M_phi checkpoint (executor calls
#                 still go to the same served model name — see src/training/README).
#
#SBATCH --job-name=sah-outer
#SBATCH --account=av_alpamayo_reasoning
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --time=04:00:00
#SBATCH --output=/lustre/fsw/portfolios/av/users/yingzim/logs/slurm/%x-%j.out
#SBATCH --error=/lustre/fsw/portfolios/av/users/yingzim/logs/slurm/%x-%j.err

set -euo pipefail
umask 027
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh

export IMAGE="${IMAGE:-/lustre/fsw/portfolios/av/users/yingzim/sqsh/dgemma-core-aarch64.sqsh}"
export REPO="$CODE_ROOT/self_adapt_harness"
export VLLM_ENV="${VLLM_ENV:-$ENV_ROOT/weave-qwen35-vllm/0.17.1}"
export MODEL_PATH="${MODEL_PATH:-$MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a}"
export SERVED_MODEL="${SERVED_MODEL:-qwen3.5-9b}"
export N_REPLICAS="${N_REPLICAS:-4}"
export ROUND_ID="${ROUND_ID:-1}"
export TASKS="${TASKS:-eft__math__circle_packing}"
export K="${K:-8}"
export MAX_EVALS="${MAX_EVALS:-20}"
export EVAL_TIMEOUT="${EVAL_TIMEOUT:-120}"
export BASES_FILE="${BASES_FILE:-}"
export MPHI_PATH="${MPHI_PATH:-}"   # merged M_phi ckpt (step>=2): replica 0 = proposer, rest = frozen M0
export ROLLOUT_PAR="${ROLLOUT_PAR:-8}"
export PROPOSE_PAR="${PROPOSE_PAR:-8}"
export PROPOSER_SEED="${PROPOSER_SEED:-$((1000 + ROUND_ID))}"
export PROTOCOL="${PROTOCOL:-sah}"  # sah (unchanged default) | adaptive_v1
export PROTOCOL_STATE="${PROTOCOL_STATE:-}"
export PROTOCOL_ROUND="${PROTOCOL_ROUND:-}"
export TOTAL_ROUNDS="${TOTAL_ROUNDS:-}"
export ROLLOUT_REPEATS="${ROLLOUT_REPEATS:-3}"
export PROMOTION_REPEATS="${PROMOTION_REPEATS:-$ROLLOUT_REPEATS}"
export ROLLOUT_SEED="${ROLLOUT_SEED:-104729}"
export PLATEAU_ROUNDS="${PLATEAU_ROUNDS:-3}"
export CONFIDENCE_Z="${CONFIDENCE_Z:-0}"

export OUT_DIR="$RUN_ROOT/self_adapt_harness/outer${OUT_TAG:+-$OUT_TAG}"
mkdir -p "$OUT_DIR"

srun --nodes=1 --ntasks=1 --cpus-per-task=64 --export=ALL \
  --container-image="$IMAGE" \
  --container-mounts="/lustre:/lustre,/tmp:/tmp" \
  --container-workdir="$REPO" \
  bash "$REPO/scripts/_outer_round_worker.sh"

echo "round dir: $OUT_DIR/round$(printf '%03d' "$ROUND_ID")"
