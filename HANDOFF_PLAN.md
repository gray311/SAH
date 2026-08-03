# HarnessRL — experiment handoff plan

Written 2026-08-02. Everything below is either verified against data/code or
explicitly marked as unverified. Read §5 (pitfalls) before running anything —
most of it is a list of ways I already wasted GPU hours.

---

## 1. Motivation and the claim under test

An agent's performance is decided as much by its **harness** (system prompt,
skills, tool descriptions, control parameters, and generated tool code) as by the
model weights. Self-improvement today takes one of two forms:

| family | what the reward updates | examples |
|---|---|---|
| **executor adaptation** | the solver's own weights | TTT-Discover, ThetaEvolve |
| **artifact / context evolution** | an external archive or harness, revised by a **fixed** proposer | AlphaEvolve, OpenEvolve, Meta-Harness |

**Our claim:** keep the executor permanently frozen and instead train the
*policy that proposes harnesses*. The proposer internalizes the task's reward
history into its weights, so the same reward buys more progress per executor
rollout than either alternative.

**The figure that must decide this** is score-vs-compute, one panel per task:
- x = cumulative **executor rollouts** actually spent by that arm (log scale)
- y = best **valid** score so far, normalized: 0 = seed program, 1.0 = published ≤10B best
- three arms, plus TTT-Discover's published Qwen3-8B point at its own 25,600-rollout budget

**Hard constraint, applies to everything:** no strong-model leakage. The frozen
Qwen3.5-9B must derive every solution itself. No stronger teacher, no external
solution, no human hint, no injected reference program. Any analyst pass must run
on the **same frozen model** and pass the leak guard.

---

## 2. The three arms (what must differ, what must not)

All arms share: the same frozen executor (Qwen3.5-9B), the same six tasks, the
same evaluator, the same fixed initial harness as the starting point, and the
same seed program. They differ **only in what gets updated**.

| arm | updates | harness | proposer | analyst |
|---|---|---|---|---|
| **A. update proposer** (ours) | φ (LoRA on proposer) | synthesized per round | trained | off |
| **B. context only** | nothing — only what the proposer *reads* | synthesized per round | frozen at base | **on** |
| **C. update executor** (TTT) | executor LoRA | **fixed initial harness** | none | off |

Arms A and B come from the same driver so they are budget-matched by
construction; arm C is a separate loop because it has no proposer.

**Six tasks for the figure** (chosen for data coverage):
```
eft__math__erdos_min_overlap      eft__math__circle_packing
eft__math__hadamard_maximal_det   eft__math__first_autocorr_ineq
eft__math__second_autocorr_ineq   eft__ahc_simpletes__ahc039
```

---

## 3. Status — what is done, what is not

### Done and verified
- **Main table** `papers/tables/proposer_update.tex` — final. `\method (initial)`,
  `\method (context)` (9/11 tasks), `\method (weight)`, plus Best Human,
  proprietary rows, Finch 2B/4B/9B, Previous SOTA.
- **Erdős crosses SOTA**: raw **0.380919** vs previous ≤10B best 0.380932, also
  past best human 0.380927. Verified clean: JAX/optax step-function optimizer the
  executor wrote itself, no hardcoded constant, no evaluator/file/network access.
- **Cross-task transfer heatmap** `papers/figures/cross_task_transfer.png` —
  12 source rows × 11 targets, zero-shot, Best@6.
  **Finding: transfer is essentially absent.** Row means span −3.4% to +0.1%
  (ahc058 excluded, its base ≈ 0 so ratios explode). Even in-task diagonal cells
  are not better than base. Amortization holds *across rounds of a task*, not
  across tasks.
- **`\method (context)` row** — from context_v2 rounds 1861–1863, each verified
  to carry 11 analyst briefs.

### Not done / blocked
- **CP-26 SOTA**: our verified best is **2.502** (a uniform 5×5+1 grid, valid:
  in-bounds, zero overlap). Target 2.635983. Two attempts failed; see §5.7.
  **The 2.635983 in the main table is not reproduced by any run we have.**
- **Cross-model transfer**: never started. The 35B endpoint
  `http://10.12.190.18:10211` was up once and has been unreachable since.
- **Arm C (TTT)**: **all data so far is invalid** — see §5.6. Must be rebuilt.
- **Arms A/B**: healthy but only ~2 rounds each (≈5 h/round for six tasks).

---

## 4. What to run

### 4.1 Arms A and B (matched)

Driver: `scripts/context_ablation.sh`. Same script for both; `TRAIN_PHI` selects
the arm.

```bash
SIX="eft__math__erdos_min_overlap eft__math__first_autocorr_ineq \
eft__math__second_autocorr_ineq eft__math__circle_packing \
eft__math__hadamard_maximal_det eft__ahc_simpletes__ahc039"

# arm A — update proposer
CTX_TASKS="$SIX" TRAIN_PHI=1 USE_ANALYST=0 K=8 MAX_EVALS=20 EVAL_TIMEOUT=300 \
  bash scripts/context_ablation.sh <n_rounds> <round_base> $RUN_ROOT/self_adapt_harness/arm_proposer

# arm B — context only
CTX_TASKS="$SIX" TRAIN_PHI=0 USE_ANALYST=1 K=8 MAX_EVALS=20 EVAL_TIMEOUT=300 \
  bash scripts/context_ablation.sh <n_rounds> <round_base> $RUN_ROOT/self_adapt_harness/arm_context_long
```

Round numbers must not collide with existing rounds (current max ≈ 1900s; pick
2000+). Budget ≈ **5 h per round** for six tasks at K=8. Aim for ≥6 rounds per
arm; run them concurrently (1 node each).

Verify arm A is really training:
```bash
grep -c 'trained -> mphi_ctxp' $RUN_ROOT/self_adapt_harness/arm_proposer/driver.log
```
If this is 0, arm A is silently identical to arm B and the comparison is void.

### 4.2 Arm C (TTT) — must be rebuilt first

Current scripts: `scripts/ttt_iterate.sbatch` (host wrapper) +
`scripts/_ttt_iter_worker.sh` (in-container loop). **The in-container loop cannot
submit training jobs** (§5.6). Restructure so that per round:

1. host `sbatch`/`srun --container` → generate K solutions with the current ckpt
2. host (outside container) → `sbatch` the LoRA training + merge, wait
3. loop with the merged ckpt

TTT-Discover's published config (arXiv:2601.16175, Table 9) — match what you can:

| parameter | their value |
|---|---|
| model | gpt-oss-120b (they also report **Qwen3-8B**, which is the ≤10B point we cite) |
| batch | **512 = 8 groups × 64 rollouts** |
| steps | **50** (⇒ 25,600 rollouts/problem) |
| LoRA rank | 32 |
| optimizer | Adam, lr 4e-5 |
| KL coefficient | 0.1 (0.01 for algorithm engineering) |
| sampling temperature | 1.0, context 32768 |
| objective | entropic utility (adaptive β + KL constraint) |

Their Qwen3-8B results, for the figure's reference point:
Erdős **0.380932**, AC1 **1.50525**, AC2 **0.9472**.

We cannot afford 25,600 rollouts/task. Whatever budget is used, **state both
budgets on the figure** — do not present it as an equal-compute comparison.

### 4.3 Cross-model transfer (not started)

Needs a second, larger frozen executor. Protocol: train the proposer only against
M0, freeze the harness bank on M0, forbid the target model from re-editing or
re-selecting harnesses, permit only chat-template/tool-call syntax adapters.
Compare `E+H₁`, `E+H_φ0`, `E+H_φj`, `M0+H_φj`.

### 4.4 Figures

```bash
python3 scripts/score_compute_curves.py    # six panels -> papers/figures/score_compute_curves.{png,pdf}
python3 scripts/cross_task_heatmap.py      # transfer heatmap
python3 scripts/arms_status.py             # budget / best / plateau per arm
python3 scripts/context_collect.py         # \method (context) row, analyst rounds only
```

---

## 5. Pitfalls — read this before running

Every item below actually happened.

**5.1 The score direction.** `rows[].score` is a *combined* score and is
**higher-is-better on every task**, including the minimized ones (Erdős, AC1).
The display-scale conversion re-applies direction. Taking `min()` for the
minimized tasks silently picks the *worst* round. This bug appeared twice
(figure script and `context_collect.py`).

**5.2 Display-scale conversions** (verified against a rollout reporting both):
```
Erdős    raw = 0.380922 / combined
AC1      raw = 1.505293 / combined
AC2      raw = combined * 0.896280
CP       sum_radii = combined * 2.635
ahc039   raw = combined * 225_000       (0.2733511 × 225000 = 61504 = total_score ✓)
ahc058   raw = combined * 4.5e8
Hadamard, EPLB, PRISM, LLM-SQL, Txn: combined IS the table value
```

**5.3 The analyst only fires when there is prior-round feedback.** Condition in
`outer_round.py`: `if SAH_ANALYSIS == "1" and fb:`. **Round 1 never has an
analyst.** Using round 1 as the "context" condition measures a cold base
proposer, not context adaptation. `context_collect.py` now verifies each round's
Slurm log for `analysis brief attached` and skips rounds with zero.

**5.4 The global-ratchet trap.** Several drivers copy the **global**
`$RUN_ROOT/self_adapt_harness/outer/best_programs.json` into the workspace after
each round. That re-imports the main campaign's incumbents and the run stops
measuring itself. `context_ablation.sh` now keeps a campaign-local ratchet;
`fresh_campaign.sh` has `NO_INHERIT=1`. **Check any new driver for this.**

**5.5 Never split one shared ratchet into "independent" arms.** The first version
of the score-compute figure plotted campaign rounds with base-φ as a separate
"context" arm with its own x-axis. Those rounds *inherit programs built by the
trained-φ rounds* (e.g. round760 is a base-φ round whose starting score 0.8583
came from earlier trained rounds), so the curve got credit for compute it never
spent and looked faster than the proposer arm. Arms must each own their ratchet.

**5.6 You cannot `sbatch` from inside the compute container.** The TTT loop ran
entirely inside the container and submitted its training jobs from there. The
submissions returned empty job IDs, `wait_job ""` spun for three hours, the merge
never appeared, and **every round re-served the base checkpoint**. All 18 TTT
jobs then hit the 4 h wall. Any "TTT round 2 vs round 1" numbers produced before
this is fixed are the *same model run twice* and mean nothing.

**5.7 Circle packing is stuck in a hard local optimum.** The 2.502 uniform grid
cannot be improved by local edits: with the ratchet on, all K=16 candidates score
*exactly* the incumbent, giving a zero-variance group
(`no_signal(true-plateau)`) → zero advantage → φ never trains. `NO_INHERIT=1`
restores the signal (φ trained 5×, scores 1.86–2.03) but removes compounding, so
it never gets back above 2.502. Warm-starting the 2.502 ratchet *with* a trained
φ re-plateaus immediately (15/15 candidates identical to base). Reaching 2.636
appears to need the executor to write a **variable-radius continuous optimizer**
(SLSQP-style), which it does not do spontaneously. Seeding such a skill would be
leakage — do not do it without an explicit decision.

**5.8 Environment gotchas.**
- `VLLM_ENV` is not exported by default: `export VLLM_ENV="${VLLM_ENV:-$ENV_ROOT/weave-qwen35-vllm/0.17.1}"`.
- The container image does **not** ship the agent package. Install first:
  `uv pip install --system -e "$CODE_ROOT/NexAU" jax optax orjson cvxpy` with
  `UV_BREAK_SYSTEM_PACKAGES=1`, then assert `from nexau import Agent`.
  Without it, rollouts return `best=None` **silently** while the job looks healthy.
- AHC tasks score **0** without native aarch64 testers:
  `AHC_NATIVE=1 AHC_CXX=g++ AHC_CASE_WORKERS=12 AHC_CACHE_DIR=$SAH/ahc_work/cache`.
- LLM-SQL needs `EVAL_TIMEOUT=420`; the default 180–240 makes every real algorithm
  time out.
- A bare `wait` also waits on the backgrounded vLLM server, which never exits.
  Track rollout PIDs and wait on those. This alone caused two 4 h timeouts where
  the rollouts had actually finished in ~25 minutes.
- **Jobs are capped at 4 h.** Size each round to fit generation + training + merge.
- Do not `pkill -f <pattern>` when the pattern also matches your own shell — it
  kills the session. Use STOP flags or explicit PIDs.

**5.9 Trainer input format.** The offline-GRPO trainer needs replay rows
`{"messages": [...], "tools": [...], "metadata": {"advantage": float, "reward": float, ...}}`
and reads tool schemas from **`metadata.tools`**. The Qwen3.5 loss-mask generator
only finds trainable tokens when the assistant turn is an **inline `<tool_call>`
block**; a plain-text assistant message yields
`offline GRPO row 0 has no trainable assistant tokens`.

**5.10 Not every job runs at 4 GPUs on one node** — check the budget (32 GPU) with
`squeue -u $USER -h -t RUNNING,PENDING -o "%D %j"`, and exclude other projects'
jobs (`dgemma_*`, `anch-*`, `v5b-*` are **not ours — never cancel them**).

---

## 6. Integrity notes that must survive into the paper

- **LLM-SQL is not a clean result.** A curated note placed a verified 0.728
  program in the task message and instructed the harness to make the executor
  adopt it *verbatim*, naming the row-sort that produces the score. That is
  solution injection. It is excluded from our best-score claims; clean count is
  best on five (Erdős, ahc039, ahc058, EPLB, PRISM) and a tie on circle packing.
  The note has been stripped from all 16 workspaces (backups: `*.withleak`).
- **Erdős had no analyst note.** An earlier draft claimed one; the audit found the
  only `analyst_note` in the entire campaign belongs to `adrs__llm_sql`.
- **The reward ceiling is the published SOTA value** (`results/finch_targets.json`,
  `sota_combined`). It normalizes the reward only and never enters the executor's
  context, but it must be disclosed.
- **A reward-hacked Transaction entry (32258, validity=0) was sitting in the global
  ratchet** and has been quarantined to the best valid parent (4184.10); backup
  `best_programs.json.with_txn_hack`.
- Claims already removed from the paper because the code does not implement them:
  checkpoint symlink rollback, a `K/2` valid-candidate training guard, and
  "generated tools cannot reach the evaluator" (they *can* call `ctx.evaluate()`;
  what is unreachable is the evaluator implementation and ground truth).

---

## 7. Key paths

```
code            $CODE_ROOT/self_adapt_harness
runs            $RUN_ROOT/self_adapt_harness
  outer/round*/round_summary.json     per-round groups, rows, scores
  outer/best_programs.json            GLOBAL ratchet (shared — treat as read-only)
  arm_proposer/, arm_context_long/    matched arms A and B
  ttt_arm/iter*/curve.jsonl           arm C curves (currently invalid, see §5.6)
  context_v2/                         context arm used for the table row
  cross_task/rows.txt, rows2.txt      transfer matrix rows (source, round, job)
checkpoints     $MODEL_ROOT/checkpoints/self_adapt_harness/
merged          $MODEL_ROOT/exports/self_adapt_harness/     (per-task adapters mphi_f_*)
base model      $MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a
paper           $CODE_ROOT/self_adapt_harness/papers
```

---

## 8. Priority order

1. **Rebuild arm C (TTT)** so training actually happens (§4.2, §5.6). Without it
   the central figure has only two of three arms.
2. **Extend arms A and B** to ≥6 rounds each so the comparison is not decided at
   2 rounds. At 16 rollouts they are within noise of each other and **context is
   ahead on 4 of 6 tasks** — the hypothesis is *not* supported at that budget, and
   this must be reported honestly whichever way it ends up.
3. Regenerate the six panels; state both budgets; do not claim equal compute.
4. Optional: cross-model transfer, and a decision on CP-26 (§5.7).
