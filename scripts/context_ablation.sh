#!/usr/bin/env bash
# \method (context) ablation — adaptation through the proposer's CONTEXT only.
#
#   context_ablation.sh <n_steps> <round_base> [workspace]
#
# The proposer's weights are NEVER updated (no train step at all).  What changes
# round to round is only what the proposer READS: the incumbent harness/program,
# the experience digest, and an analyst brief produced by the FROZEN executor.
# This isolates context adaptation from weight adaptation, and is the row that
# separates "harness search helps" from "training the proposer helps".
#
# Leakage discipline (the whole point of this run):
#   * proposer = frozen base = same weights as the executor (no stronger model)
#   * analyst  = the SAME frozen model, via SAH_ANALYSIS_BASE_URL
#   * SAH_LEAK_NEUTRALIZE=1 scrubs the brief before it reaches the proposer
#   * no curated notes: any analyst_note in the feedback file is stripped below
set -uo pipefail
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
SAH="$CODE_ROOT/self_adapt_harness"
OUT="$RUN_ROOT/self_adapt_harness/outer"
NSTEPS="${1:?usage: context_ablation.sh <n_steps> <round_base> [ws]}"
RBASE="${2:?}"
WS="${3:-$RUN_ROOT/self_adapt_harness/context_ablation}"
mkdir -p "$WS"
log(){ echo "[$(date -Is)] [ctx] $*"; }

# AHC tasks score 0 unless the natively-rebuilt aarch64 testers are used (the
# stock x86 binaries fail silently under qemu). Harmless for the other tasks.
export AHC_NATIVE=1 AHC_CXX=g++ AHC_CASE_WORKERS=12 AHC_CACHE_DIR="$SAH/ahc_work/cache"

TASKS_ALL="${CTX_TASKS:-eft__math__erdos_min_overlap eft__math__first_autocorr_ineq eft__math__second_autocorr_ineq eft__math__circle_packing eft__math__hadamard_maximal_det eft__ahc_simpletes__ahc039 eft__ahc_simpletes__ahc058 adrs__eplb adrs__prism adrs__llm_sql adrs__txn_scheduling}"

# seed the harness base from the fixed initial harness (same start as the other rows)
bases="$WS/round000_bases.json"
if [ ! -f "$bases" ]; then
  python3 - "$bases" "$SAH" <<'PY'
import json,sys
out,sah=sys.argv[1],sys.argv[2]
tasks="eft__math__erdos_min_overlap eft__math__first_autocorr_ineq eft__math__second_autocorr_ineq eft__math__circle_packing eft__math__hadamard_maximal_det eft__ahc_simpletes__ahc039 eft__ahc_simpletes__ahc058 adrs__eplb adrs__prism adrs__llm_sql adrs__txn_scheduling".split()
json.dump({t:{"package":f"{sah}/src/inner/harness","score":0.0} for t in tasks}, open(out,"w"), indent=1)
print("seeded initial-harness bases for", len(tasks), "tasks")
PY
fi

wait_job(){
  local J="$1"
  while :; do
    local S; S=$(squeue -j "$J" -h -o %T 2>/dev/null | head -1)
    case "$S" in PENDING|RUNNING|COMPLETING) sleep 60; continue ;; esac
    local ST; ST=$(sacct -j "$J" -X -n -o State 2>/dev/null | head -1 | xargs)
    case "$ST" in PENDING|RUNNING|COMPLETING|"") sleep 60 ;; *) return 0 ;; esac
  done
}

for i in $(seq 0 $((NSTEPS-1))); do
  [ -f "$WS/STOP" ] && { log "STOP flag"; break; }
  R=$((RBASE+i)); RD="$OUT/round$(printf '%03d' "$R")"
  log "step $((i+1))/$NSTEPS: round$R over ${TASKS_ALL// /,}"
  JOB=""
  for _ in $(seq 1 20); do
    RAW=$(cd "$SAH" && env ROUND_ID="$R" TASKS="$TASKS_ALL" \
      K="${K:-8}" MAX_EVALS="${MAX_EVALS:-20}" EVAL_TIMEOUT="${EVAL_TIMEOUT:-420}" \
      FORCE_TOOL_FRAC="${FTF:-0.25}" SAH_MIN_ITERS="${SAH_MIN_ITERS:-0}" \
      SAH_ADV=v3 SAH_ANALYSIS=1 SAH_LEAK_NEUTRALIZE=1 \
      BASES_FILE="$bases" MPHI_PATH="" \
      SEED_PROGRAMS_FILE="$WS/best_programs.json" \
      FEEDBACK_FILE="$WS/task_feedback.json" \
      sbatch --parsable scripts/outer_round.sbatch 2>&1)
    JOB=$(echo "$RAW" | grep -oE '[0-9]{6,}' | tail -1)
    [ -n "$JOB" ] && break; sleep 60
  done
  [ -n "$JOB" ] || { log "submit failed: $(echo "$RAW"|tail -1)"; break; }
  log "  job $JOB"; wait_job "$JOB"

  [ -f "$RD/round.json" ] && [ ! -f "$RD/round_summary.json" ] && \
    (cd "$SAH/src" && python3 -m outer.outer_round collect --round-dir "$RD") >/dev/null 2>&1
  [ -f "$RD/round_summary.json" ] || { log "no summary — stop"; break; }

  # carry the ratchet + feedback forward; NEVER carry a curated note
  [ -f "$OUT/best_programs.json" ] && cp "$OUT/best_programs.json" "$WS/best_programs.json" 2>/dev/null
  [ -f "$OUT/task_feedback.json" ] && cp "$OUT/task_feedback.json" "$WS/task_feedback.json" 2>/dev/null
  python3 - "$WS/task_feedback.json" <<'PY'
import json,sys,os
f=sys.argv[1]
if os.path.exists(f):
    d=json.load(open(f)); n=0
    for t,e in d.items():
        if isinstance(e,dict) and e.pop("analyst_note",None) is not None: n+=1
    if n: json.dump(d,open(f,"w"),indent=1); print(f"  stripped {n} curated note(s)")
PY
  bases="$RD/next_bases.json"
  python3 - "$RD/round_summary.json" <<'PY'
import json,sys
g=json.load(open(sys.argv[1]))["groups"]
for t,v in sorted(g.items()):
    print(f"  {t:38s} best={v.get('best_score')} improved={v.get('improved')}")
PY
  log "  phi UNCHANGED (context-only ablation)"
done
log "context ablation done"
