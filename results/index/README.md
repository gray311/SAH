# Experiment index — the storage contract

One stable format for **evaluation** results across the project, cut along the
three axes that matter for this work:

| axis | file | grain | answers |
|------|------|-------|---------|
| **task** | `tasks.jsonl` | 1 row / task | what the benchmark is, which metric, which direction, what to compare against |
| **method** | `methods.jsonl` | 1 row / method | which model variant + which methodology produced a number |
| **metric — performance** | `exps/<exp_id>/steps.jsonl` | 1 row / step | how the search *progressed* |
| **metric — compute** | `exps/<exp_id>/rollouts.jsonl` | 1 row / rollout | what that progression *cost* |

`steps` is the y-axis, `rollouts` is the x-axis. Together they must let you plot
performance against compute **without missing anything** — which is why
`rollouts.jsonl` also carries non-rollout compute (proposal, training, serving)
as its own rows, so the total closes.

Everything is JSONL: append-only, greppable, diffable, no dependencies.

```
results/index/
  README.md               <- this contract
  schema/*.schema.json    <- field-level spec for each table (the normative source)
  tasks.jsonl             <- dimension, shared by all experiments
  methods.jsonl           <- dimension, shared by all experiments
  exps/
    _example/             <- synthetic, illustrative; not real data
    <exp_id>/
      exp.json            <- manifest: what was parsed, from where, what is missing
      rollouts.jsonl      <- compute facts
      steps.jsonl         <- performance facts
```

Raw artifacts live on the cluster under `$RUN_ROOT` and are **not** mounted in
this checkout. Parsing happens where they live; the compact extract is committed
here and is usable offline.

```
$RUN_ROOT/.../roundNNN/   --parse-->   results/index/exps/<exp_id>/   -->   plots, tables
```

To add an experiment, use the **`exp-index`** skill — it walks the raw artifacts,
fills what can be measured, and asks you for the method metadata that was never
written down.

## Keys

| key | form | example |
|-----|------|---------|
| `task_id` | `<suite>__<family>__<name>`, or 2 segments for ADRS — unchanged from the code registry | `eft__math__circle_packing`, `adrs__eplb` |
| `method_id` | kebab slug, assigned once, **never reused or redefined** | `mphi-freshall-2026-08` |
| `exp_id` | kebab slug, conventionally `<workspace>-<lo_round>-<hi_round>` | `freshall-cp-310-317` |
| `rollout_id` | `<exp_id>/<task_id>/r<round>/k<kk>[/<run_idx>]` | `freshall-cp-310-317/eft__math__circle_packing/r312/k03/0` |
| step | `(rollout_id, step)` | — |

A config change means a **new** `method_id`. Editing a method in place silently
rewrites the meaning of every number already attributed to it.

## Two scales, always both

Every task has a **raw** metric on the paper's scale (`c5`, `c1`, `c2`,
`sum_radii`, `det_ratio`, AHC score sums) and a normalised `combined_score` that
is **always higher-is-better**. `tasks.jsonl` carries the direction and the
conversion so no analysis hardcodes a formula:

| `to_combined.kind` | meaning | tasks |
|---|---|---|
| `identity` | `combined = raw` | the four ADRS tasks, hadamard |
| `divide_by` | `combined = raw / const` | cp, ac2, ahc039, ahc058 |
| `const_over` | `combined = const / raw` (raw is lower-better) | erdos, ac1 |

**Facts are always stored in `combined_score`.** Raw values are derived on read.
Two AHC constants are marked `DERIVED` in `tasks.jsonl` — they were fitted from
published pairs, not taken from a stated formula; verify before publishing.

## Step semantics that must not be flattened

`steps.jsonl` normalises three traps in the raw artifacts:

- **probe** steps are subsampled, off-budget, and never update best-so-far — they
  are *not* comparable to full evaluations, and they are not free either.
- **seed** step 0 is evaluated then refunded from the budget; it is the baseline,
  not agent work. It *does* set the initial best-so-far, so a curve starts at
  `(evals_used = 0, best_so_far = seed_score)`.
- **note** steps are audit text carrying best-so-far as filler, not a measurement.

Three derived fields mean a reader needs none of this context:
`counts_against_budget`, `evals_used` (cumulative budgeted evaluations), and
`best_so_far` (monotone, probe- and note-excluded). A perf-vs-compute curve is
then simply `(evals_used, best_so_far)`.

## Compute must close

Every `rollouts.jsonl` row has a `kind`:

| `kind` | what it is | has a score? |
|---|---|---|
| `rollout` | one inner `M0 + H2` search | yes |
| `proposal` | `M_phi + H1` generating a round's candidates for a task | no |
| `invalid_candidate` | generation cost of a candidate that failed validation and never ran | no |
| `training` | the GRPO/LoRA update for a round | no |
| `serving` | GPU time held by the vLLM job | no |

Summing over all rows gives the true cost. Summing only `kind="rollout"`
**undercounts** — which is exactly what this field exists to prevent.

Under an evaluation cascade one candidate has several rollout rows (distinct
`run_idx`, `stage` of `screen`/`full`). For **score**, take the argmax across
them; for **compute**, take the **sum**. Screening cost is what the cascade
trades away, so dropping it flatters the method.

## Never guess a missing number

A compute field that was not actually measured is `null`, and `compute_flags`
records why (`measured` / `derived` / `partial` / `unmetered`). **A zero would
silently make a method look cheap.** `exp.json` repeats this as `cost_complete`
plus an `unattributed` list, so plots can mark or exclude experiments whose cost
axis is incomplete.

The same rule governs `methods.jsonl`: fields the artifacts never recorded
(advantage mode, LoRA checkpoint, cascade on/off) are `null` and listed in
`unknown_fields`. Those are filled by **asking the user** — never inferred from
filesystem paths, directory dates, or what a sibling experiment happened to use.

## Known-incomplete by construction

As of format version 1, these consumers are unmetered in the raw artifacts, so
every experiment parsed from them will have `cost_complete: false` until the
instrumentation changes:

- **LLM tokens** — `llm_input_tokens` / `llm_output_tokens` exist in the ledger
  but are never assigned; always absent. `llm_calls` is back-derived by counting
  assistant messages, and is lost entirely if the agent crashed.
- **Proposer cost** — only a per-candidate `llm_calls` integer survives; no
  tokens, no wall-clock.
- **Probe wall time** — recorded per step, but not accumulated into the rollout
  ledger's `sandbox_seconds`.
- **Training step** — no accounting at all.
- **vLLM serving GPU-time** — likely the dominant real cost; recoverable only
  from Slurm records, which nothing links to round directories.
