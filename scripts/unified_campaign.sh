#!/usr/bin/env bash
# One clean entry point for the two proposer-training modes:
#   bash scripts/unified_campaign.sh sah <fresh_campaign.sh args...>
#   bash scripts/unified_campaign.sh adaptive_v1 <task> <rounds> <round_base> [workspace]
#
# `sah` delegates byte-for-byte to the existing campaign. `adaptive_v1` keeps
# SAH's serving/inner/training stack, but uses sequential semantic proposals,
# repeated matched outcomes, dual frontiers, and plateau-triggered training.
set -euo pipefail

MODE="${1:?usage: unified_campaign.sh <sah|adaptive_v1> ...}"
shift
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAH="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ "$MODE" = "sah" ]; then
  exec bash "$SCRIPT_DIR/fresh_campaign.sh" "$@"
fi
if [ "$MODE" != "adaptive_v1" ]; then
  echo "unknown mode: $MODE (expected sah or adaptive_v1)" >&2
  exit 2
fi

source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
TASK="${1:?adaptive_v1 requires task_id}"
NROUNDS="${2:?adaptive_v1 requires number of rounds}"
ROUND_BASE="${3:?adaptive_v1 requires absolute starting round}"
TAG="$(echo "$TASK" | sed 's/.*__//; s/_//g' | cut -c1-8)"
WORKSPACE="${4:-$RUN_ROOT/self_adapt_harness/adaptive_v1_$TAG}"
OUT_TAG="${OUT_TAG:-adaptive-v1-$TAG}"
OUT="$RUN_ROOT/self_adapt_harness/outer-$OUT_TAG"
STATE="$WORKSPACE/adaptive_v1_state.json"
mkdir -p "$WORKSPACE" "$OUT"
LOG="$WORKSPACE/campaign.log"
log(){ echo "[$(date -Is)] [adaptive_v1:${TASK##*__}] $*" | tee -a "$LOG"; }

bases=""
merged_phi=""
previous_ckpt=""
start_index=0

run_training_update(){
  local round_dir="$1" manifest="$2"
  local batch="$round_dir/adaptive_train_batch.jsonl"
  local train_log="$round_dir/train_submit.log"
  local update_index step_tag train_job merge_job train_state merge_state
  update_index="$(python3 - "$STATE" "$TASK" <<'PY'
import json, sys
print(json.load(open(sys.argv[1]))["tasks"][sys.argv[2]]["controller"]["policy_updates"])
PY
)"
  step_tag="$(printf 'av1_%s_u%03d' "$TAG" "$update_index")"
  log "pending signed batch: ensuring proposer update $step_tag"

  if [ -s "$train_log" ]; then
    train_job="$(grep -oP 'train job: \K[0-9]+' "$train_log" | tail -1)"
    merge_job="$(grep -oP 'merge job: \K[0-9]+' "$train_log" | tail -1)"
    [ -n "$train_job" ] && [ -n "$merge_job" ] || {
      log "existing train log has no complete job IDs; refusing duplicate submission"
      exit 1
    }
    log "resuming existing train=$train_job merge=$merge_job"
  else
    log "submitting proposer update $step_tag"
    if [ -n "$previous_ckpt" ]; then
      BATCH_FILE="$batch" ARCHIVE_MIX=0 \
        bash "$SCRIPT_DIR/train_mphi_step.sh" \
        "$round_dir" "$step_tag" "$previous_ckpt" | tee "$train_log"
    else
      BATCH_FILE="$batch" ARCHIVE_MIX=0 \
        bash "$SCRIPT_DIR/train_mphi_step.sh" \
        "$round_dir" "$step_tag" | tee "$train_log"
    fi
    train_job="$(grep -oP 'train job: \K[0-9]+' "$train_log" | tail -1)"
    merge_job="$(grep -oP 'merge job: \K[0-9]+' "$train_log" | tail -1)"
    [ -n "$train_job" ] && [ -n "$merge_job" ] || {
      log "trainer did not return train/merge job IDs"
      exit 1
    }
  fi

  while squeue -j "$train_job" -h -o '%T' 2>/dev/null \
    | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do
    sleep 120
  done
  train_state="$(sacct -j "$train_job" -X -n -o State | head -1 | xargs)"
  [ "$train_state" = "COMPLETED" ] || {
    log "training failed ($train_state); state remains uncommitted"
    exit 1
  }
  while squeue -j "$merge_job" -h -o '%T' 2>/dev/null \
    | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do
    sleep 60
  done
  merge_state="$(sacct -j "$merge_job" -X -n -o State | head -1 | xargs)"
  [ "$merge_state" = "COMPLETED" ] || {
    log "merge failed ($merge_state); state remains uncommitted"
    exit 1
  }

  merged_phi="$MODEL_ROOT/exports/self_adapt_harness/mphi_$step_tag"
  previous_ckpt="$MODEL_ROOT/checkpoints/self_adapt_harness/mphi_$step_tag"
  find "$merged_phi" -maxdepth 1 -name '*.safetensors' -print -quit \
    | grep -q . || { log "merged checkpoint missing: $merged_phi"; exit 1; }
  (
    cd "$SAH/src"
    python3 -m protocols.adaptive_v1 commit-update \
      --state "$STATE" --manifest "$manifest" \
      --adapter "$merged_phi" --checkpoint "$previous_ckpt"
  ) | tee -a "$LOG"
  log "proposer update committed -> $merged_phi"
}

load_resume_state(){
  local status_file="$WORKSPACE/campaign_status.json"
  (
    cd "$SAH/src"
    python3 -m protocols.adaptive_v1 campaign-status \
      --state "$STATE" --task "$TASK"
  ) > "$status_file"
  mapfile -t resume_fields < <(python3 - "$status_file" "$WORKSPACE/resume_bases.json" <<'PY'
import json, sys
status = json.load(open(sys.argv[1]))
bases_path = sys.argv[2]
working = status.get("working")
if working:
    seed_score = working.get("seed_score")
    if seed_score is None:
        raise SystemExit("working frontier lacks seed_score; cannot resume safely")
    json.dump(
        {
            status["task_id"]: {
                "package": working["package"],
                "score": working["score"],
                "seed_score": seed_score,
            }
        },
        open(bases_path, "w"),
        indent=2,
    )
print(status["next_protocol_round"])
print((status.get("active_adapter") or {}).get("path") or "")
print((status.get("active_adapter") or {}).get("checkpoint_path") or "")
print(bases_path if working else "")
print((status.get("pending_training") or {}).get("manifest_path") or "")
PY
)
  start_index="${resume_fields[0]}"
  merged_phi="${resume_fields[1]}"
  previous_ckpt="${resume_fields[2]}"
  bases="${resume_fields[3]}"
  pending_manifest="${resume_fields[4]}"
}

load_resume_state
if [ -n "$merged_phi" ]; then
  find "$merged_phi" -maxdepth 1 -name '*.safetensors' -print -quit \
    | grep -q . || { log "state adapter missing: $merged_phi"; exit 1; }
fi
if [ -n "$previous_ckpt" ] && [ ! -d "$previous_ckpt" ]; then
  log "state checkpoint missing: $previous_ckpt"
  exit 1
fi
if [ -n "$bases" ]; then
  resume_package="$(python3 - "$bases" "$TASK" <<'PY'
import json, sys
print(json.load(open(sys.argv[1]))[sys.argv[2]]["package"])
PY
)"
  [ -f "$resume_package/agent.yaml" ] || {
    log "state working package missing: $resume_package"
    exit 1
  }
fi
if [ -n "$pending_manifest" ]; then
  [ -f "$pending_manifest" ] || {
    log "pending training manifest missing: $pending_manifest"
    exit 1
  }
  run_training_update "$(dirname "$pending_manifest")" "$pending_manifest"
  load_resume_state
fi
log "resume: next_protocol_round=$start_index proposer=${merged_phi:-base}"

for index in $(seq "$start_index" $((NROUNDS - 1))); do
  [ -f "$WORKSPACE/STOP" ] && { log "STOP flag found"; break; }
  round=$((ROUND_BASE + index))
  round_dir="$OUT/round$(printf '%03d' "$round")"
  if [ -e "$round_dir/round.json" ] || [ -e "$round_dir/round_summary.json" ]; then
    log "partial/untracked artifact round exists: $round_dir; refusing overwrite"
    exit 1
  fi
  log "round $round ($((index + 1))/$NROUNDS), proposer=${merged_phi:-base}"

  submit=(
    env
    "PROTOCOL=adaptive_v1"
    "PROTOCOL_STATE=$STATE"
    "PROTOCOL_ROUND=$index"
    "TOTAL_ROUNDS=$NROUNDS"
    "ROUND_ID=$round"
    "TASKS=$TASK"
    "K=${K:-4}"
    "MAX_EVALS=${MAX_EVALS:-20}"
    "ROLLOUT_REPEATS=${ROLLOUT_REPEATS:-3}"
    "PROMOTION_REPEATS=${PROMOTION_REPEATS:-3}"
    "ROLLOUT_SEED=${ROLLOUT_SEED:-104729}"
    "PLATEAU_ROUNDS=${PLATEAU_ROUNDS:-3}"
    "CONFIDENCE_Z=${CONFIDENCE_Z:-0}"
    "OUT_TAG=$OUT_TAG"
    "PROPOSER_SEED=${PROPOSER_SEED:-23}"
  )
  [ -n "$bases" ] && submit+=("BASES_FILE=$bases")
  [ -n "$merged_phi" ] && submit+=("MPHI_PATH=$merged_phi")
  [ -f "$OUT/best_programs.json" ] && \
    submit+=("SEED_PROGRAMS_FILE=$OUT/best_programs.json")

  raw="$(cd "$SAH" && "${submit[@]}" sbatch --parsable scripts/outer_round.sbatch)"
  job="$(echo "$raw" | grep -oE '[0-9]{6,}' | tail -1)"
  [ -n "$job" ] || { log "outer submission failed: $raw"; exit 1; }
  log "outer job $job"
  while squeue -j "$job" -h -o '%T' 2>/dev/null \
    | grep -qE 'PENDING|RUNNING|CONFIGURING|COMPLETING'; do
    sleep 120
  done
  [ -f "$round_dir/round_summary.json" ] || {
    log "round $round has no summary; stopping"
    exit 1
  }
  bases="$round_dir/next_bases.json"

  manifest="$round_dir/adaptive_train_manifest.json"
  if [ ! -f "$manifest" ]; then
    decision="$(python3 - "$round_dir" "$TASK" <<'PY'
import json, sys
print(json.load(open(f"{sys.argv[1]}/round_summary.json"))["groups"][sys.argv[2]]["training_decision"])
PY
)"
    log "no proposer update: $decision"
    continue
  fi

  run_training_update "$round_dir" "$manifest"
done
log "campaign finished; state=$STATE"
