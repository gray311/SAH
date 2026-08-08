#!/usr/bin/env bash
# Real executor replay for the authoritative runtime component contract.

#SBATCH --job-name=sah-ac2-c03-contract
#SBATCH --account=av_alpamayo_reasoning
#SBATCH --partition=pool0
#SBATCH --qos=av_alpamayo_reasoning_low
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=01:30:00
#SBATCH --no-requeue
#SBATCH --output=/lustre/fsw/portfolios/av/users/yingzim/runs/slurm/%x-%j.out
#SBATCH --error=/lustre/fsw/portfolios/av/users/yingzim/runs/slurm/%x-%j.err

set -euo pipefail
umask 027
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh

readonly RUN_DIR="$RUN_ROOT/campaigns/debug-evolve-qwen35-6186121"
readonly INNER="$RUN_DIR/inspection/ac2_round001/contract_replay_cand03_inner.sh"
test -r "$SAH_IMAGE"
test -x "$VLLM_ENV/bin/vllm"
test -x "$INNER"
mkdir -p "$RUN_ROOT/slurm"

srun --nodes=1 --ntasks=1 --cpus-per-task="$SLURM_CPUS_PER_TASK" \
  --container-image="$SAH_IMAGE" \
  --container-mounts=/lustre/fsw:/lustre/fsw \
  --no-container-mount-home \
  --container-workdir="$SAH_ROOT" \
  /bin/bash "$INNER"
