---
name: exp-index
description: Parse a raw SAH experiment (outer-loop round dirs, baseline job outputs, or a published table) into the evaluation index at results/index/exps/<exp_id>/. Use whenever asked to index, ingest, import, or record experiment results; to add a run to the index; to backfill old campaigns; or to make results plottable as performance-vs-compute. Interviews the user for method metadata the raw artifacts never recorded.
---

# Parsing an experiment into the index

The index at `results/index/` stores evaluation results along three axes — task,
method, and metric (performance per step, compute per rollout). Read
`results/index/README.md` first; it is the contract, and
`results/index/schema/*.schema.json` is the normative field spec. A worked
example of every row type is in `results/index/exps/_example/`.

Your job here is a **parse plus an interview**. The artifacts give you the
numbers; only the user can give you the method. Do not substitute one for the
other.

## The one rule

> **Never invent a number, and never let a gap look like a zero.**

Compute that was not measured is `null` with a `compute_flags` entry saying why.
Method fields nobody recorded are `null` and listed in `unknown_fields`. An
experiment with open questions carries them in `exp.json:open_questions` and is
not publication-ready. Silently filling a blank is the single most damaging
thing you can do here — a fabricated cost makes a method look efficient and
nobody downstream can tell.

## Workflow

### 1. Locate the raw artifacts

Ask the user where the experiment lives if they have not said. Raw artifacts sit
on the cluster under `$RUN_ROOT` and are **not mounted in every checkout** — if
`$RUN_ROOT` is unset, say so and stop rather than guessing paths. Confirm the
shape before parsing:

| shape | looks like | parse via |
|---|---|---|
| outer-loop campaign | `roundNNN/` dirs with `round.json`, `rollouts/`, `round_summary.json` | `references/raw-artifact-map.md` |
| baseline job | `summary.json` + per-task result JSONs from `run_baseline` | same map, single-rollout case |
| published numbers | a table in a paper or README, no artifacts | dimension rows only — no `exps/` entry |

Published baselines (Qwen3.5-9B, Finch-9B, SOTA) belong in `tasks.jsonl:references`
and `methods.jsonl`, **not** in an `exps/` directory. They have no steps and no
measurable compute; forcing them into a fact table invents a rollout that never
happened.

### 2. Establish the method — interview, do not infer

Before parsing a single number, settle which `method_id` this experiment belongs
to. Check `results/index/methods.jsonl` for an existing match.

**A config change means a new `method_id`.** Never edit an existing method in
place: that silently rewrites the meaning of every number already attributed to
it. If the experiment differs from an existing method in any recorded field, it
is a new method.

Ask the user, in one batch, whichever of these the artifacts do not answer:

- Which `method_id` does this belong to — an existing one, or a new one? If new,
  what should it be called and what is its one-line label for a plot legend?
- **Proposer**: which `M_phi` checkpoint served this (`mphi_sNNN`)? Is it on the
  trunk or a rolled-back branch?
- **Algorithm**: advantage mode (`SAH_ADV` `legacy` vs `v2`), `SAH_ALPHA`, group
  size `K`, KL coefficient, reward transform.
- **Search mechanisms**: cascade on/off and its top-N, program inheritance,
  crossover parents, stall-restart, probe availability, analyst notes injected.
- **Genome**: fixed-field spec or generative `h2spec/1.0`.
- **Budget**: evaluations per rollout, and **how many seeds** — one seed means
  no error bars, which every downstream plot must state.
- Did the config change *mid-experiment*? If yes, the span must be **split** into
  several `method_id`s; ask where the boundaries fall.

That last question matters more than it looks. Two placeholder rows already in
`methods.jsonl` (`mphi-campaign-2026-07`, `mphi-freshall-2026-08`) are marked
PLACEHOLDER precisely because they span checkpoint rollbacks and mid-flight
mechanism changes. Do not attach new experiments to a placeholder without
resolving it with the user first.

Anything the user does not know stays `null` and goes in `unknown_fields`. That
is a fine outcome; a guess is not.

### 3. Parse facts

Follow `references/raw-artifact-map.md` field by field. It maps every raw
artifact key to its index field, and lists the traps: seed refunding, probe
semantics, note rows, cascade run pairing, invalid candidates, and which ledger
fields are dead.

Write in combined scale only. Raw paper-scale values are derived on read via
`tasks.jsonl:raw_metric.to_combined`.

Order of work: `exp.json` skeleton → `rollouts.jsonl` → `steps.jsonl` → fill
`counts` and `unattributed` in `exp.json`.

### 4. Check before writing

Run these; every one has caught a real defect in this project's data:

- **Compute closes.** Every candidate in `round.json` appears in `rollouts.jsonl`
  as either a `rollout` (possibly several, under a cascade) or an
  `invalid_candidate`. A round with a `grpo_batch.jsonl` has a `training` row.
- **Cascade pairing.** A candidate with multiple `run_idx` values: score is the
  **argmax** across them, compute is the **sum**. Taking "last file wins" for the
  score is a known past bug — it banked a program that did not match its score.
- **Budget monotonicity.** Within a rollout, `evals_used` is non-decreasing, and
  its final value equals the rollout's `compute.evaluator_calls`. A mismatch
  means a step kind was misclassified.
- **Best-so-far monotonicity.** `best_so_far` never decreases, and never advances
  on a `probe` or `note` step.
- **Curve endpoints.** Every rollout's first step is `seed` at `evals_used = 0`.
- **No zero-for-null.** Grep the extract for `0` in a compute field flagged
  `unmetered`. Zero means measured-and-zero; `null` means not measured.
- **Foreign keys.** Every `task_id` is in `tasks.jsonl`, every `method_id` is in
  `methods.jsonl`.
- **Sanity against known references.** Compare per-task best scores to
  `tasks.jsonl:references`. A result far above `sota_le10b` is more likely a
  parse error, a scale mix-up, or reward hacking than a breakthrough — flag it to
  the user rather than recording it quietly.

### 5. Report

Tell the user, plainly:

- the `exp_id`, `method_id`, round span, tasks, and row counts;
- **what is unattributed** and therefore why `cost_complete` is `false`;
- any open questions still unanswered;
- anything that looked wrong (scores above SOTA, missing rollout dirs, crashed
  agents with lost `llm_calls`, cascade pairs that disagree).

If the extract is incomplete, say so directly. Do not present a partial index as
finished.

## Adding a new task

If the experiment covers a task not yet in `tasks.jsonl`, add a dimension row.
The conversion between the paper's raw metric and `combined_score` is the part to
get right — ask the user for the formula rather than fitting one from two data
points. Where a constant *was* fitted (both AHC tasks), the `derivation` field
says `DERIVED, verify` and it must stay that way until someone confirms it.

## Live writes

A running job can append rows to `exps/<exp_id>/rollouts.jsonl` and `steps.jsonl`
as it goes — the format is append-only for exactly this reason. Each parallel
campaign must write its **own** `exp_id` directory; concurrent appends to one
file from several processes are not safe.
