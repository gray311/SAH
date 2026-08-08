# Raw artifact → index field map

Field-by-field mapping from the SAH run artifacts to the index tables, plus every
trap that has produced a wrong number in this project before.

## Source layout

One outer-loop campaign workspace:

```
<outer_root>/                          # e.g. $RUN_ROOT/self_adapt_harness/fresh_all/<task>
  roundNNN/
    round.json            # proposal metadata + per-candidate validation
    prompts.json          # H1 user message per task
    trajectories.json     # H1 tool-call trajectory + raw submission per candidate
    round_summary.json    # GRPO groups: reward, advantage, best_k, improved
    next_bases.json
    grpo_batch.jsonl      # training rows — its existence means a training step ran
    tasks/<task>/candNN/  # materialised NexAU package + meta.json
    rollouts/<task>/candNN/<run_idx>/results/*.json      # THE inner result
    rollouts/<task>/candNN/<run_idx>/checkpoints/*.json  # wall-safe fallback
  best_programs.json      # cross-round program ratchet
  task_feedback.json      # per-task digest carried into the next visit
```

A baseline job (`run_baseline`) instead writes `summary.json` plus one JSON per
task, in the same inner-result shape.

## Inner result JSON → `rollouts.jsonl` + `steps.jsonl`

The file at `rollouts/<task>/candNN/<run_idx>/results/*.json` is the primary
source. It is the serialised inner session.

| raw key | index field | notes |
|---|---|---|
| `task_id` | `task_id` | already the namespaced id; do not rewrite |
| `best_score` | `best_score` | combined scale |
| `best_metrics` | `best_metrics` | raw evaluator metrics at the best step |
| `seed_score` | `seed_score` | |
| `stop_reason` | `stop_reason` | |
| `error` | `error` | |
| `ledger.evaluator_calls` | `compute.evaluator_calls` | flag `measured` |
| `ledger.probe_calls` | `compute.probe_calls` | flag `measured` |
| `ledger.edit_calls` | `compute.edit_calls` | flag `measured` |
| `ledger.llm_calls` | `compute.llm_calls` | flag **`derived`** — see traps |
| `ledger.llm_input_tokens` | `compute.llm_input_tokens` | **always ignore**; write `null`, flag `unmetered` |
| `ledger.llm_output_tokens` | `compute.llm_output_tokens` | same |
| `ledger.sandbox_seconds` | `compute.sandbox_seconds` | flag **`partial`** — see traps |
| — | `compute.wall_seconds`, `compute.gpu_seconds` | `null`, flag `unmetered` |
| `steps[]` | one `steps.jsonl` row each | see below |

If `results/*.json` is absent, fall back to `checkpoints/*.json` — it carries
`best_score`, `best_metrics`, `evaluations`, and `best_program` but **no steps**.
Record the rollout with `steps` omitted and note the truncation; do not
reconstruct a curve from a single endpoint.

### `steps[]` → `steps.jsonl`

| raw key | index field |
|---|---|
| `step` | `step` |
| `kind` | `kind` (`seed`\|`diff`\|`full_rewrite`\|`edit_eval`\|`probe`\|`note`) |
| `combined_score` | `combined_score` (`null` when `kind == "note"`) |
| `validity` | `validity` |
| `error` | `error` |
| `wall_s` | `wall_s` |
| `is_new_best` | `is_new_best` |
| `edit_note` | `edit_note` |

Three fields are **derived by you**, so readers need no task semantics:

- `counts_against_budget` = `kind in {diff, full_rewrite, edit_eval}`.
- `evals_used` = running count of `counts_against_budget` steps, inclusive.
- `best_so_far` = running max of `combined_score` over steps whose `kind` is in
  `{seed, diff, full_rewrite, edit_eval}` — **seed included, probe and note
  excluded**.
- `is_measurement` = `kind != "note"`.

## `round.json` → proposal, invalid candidates, identity

| raw path | index field |
|---|---|
| `round` | `round` |
| `per_task[tid].base_score` | `base_score` on each rollout of that task |
| `per_task[tid].seed_score` | `seed_score` fallback if the inner result lacks it |
| `per_task[tid].candidates[].k` | `k` |
| `per_task[tid].candidates[].valid` | `status` (`ok` / `invalid`) |
| `per_task[tid].candidates[].spec_hash` | `spec_hash` — the harness genome's content address |
| `per_task[tid].candidates[].changed_fields` | `changed_fields` |
| `per_task[tid].candidates[].errors` | `error` on an `invalid_candidate` row |
| `per_task[tid].candidates[].llm_calls` | generation cost (see below) |
| `per_task[tid].candidates[].review_log` | `notes` — dropped generated tools |
| `h1_version`, `h1_package_hash` | `methods.jsonl:proposer` (dimension, not fact) |
| `proposer.model`, `.seed` | `methods.jsonl:proposer` |
| `max_evals`, `k` | `methods.jsonl:budget` / `algorithm.k` |

**Generation cost is split so it is counted exactly once:**

- one `proposal` row per (round, task), `compute.llm_calls` = sum over the
  **valid** candidates;
- one `invalid_candidate` row per invalid candidate, carrying its **own**
  `llm_calls`.

## `round_summary.json` → reward signal

`groups[tid].rows[]` keyed by `k` gives `reward`, `advantage`, `score`, `valid`.
Attach these to the matching rollout row. `groups[tid].best_k` and `improved`
describe the round, not a rollout — put them in `exp.json:notes` if useful.

## `grpo_batch.jsonl` → training row

Its existence means the update ran. Emit one `kind: "training"` row for the round
with `task_id: null` and every compute field `null`/`unmetered`. Emitting it with
no numbers is the point: the gap becomes **visible** instead of absent.

## Serving

vLLM GPU time is not in any artifact. If the user supplies Slurm job ids and
elapsed times, add a `kind: "serving"` row with `gpu_seconds` flagged `measured`
or `derived`. Otherwise emit nothing and list it in `exp.json:unattributed`.

---

# Traps

Each of these has produced a wrong number here before.

**Cascade double-runs.** One candidate can have several `<run_idx>/` dirs
(successive halving: a screen pass, then a full pass). Emit one rollout row per
run_idx. For **score**, take the argmax across them — taking the last file wins
was a real bug that banked a program not matching its score. For **compute**,
take the **sum**: screening cost is exactly what the cascade trades away, and
dropping it flatters the method.

**The seed is refunded.** `seed_baseline()` evaluates the seed, then decrements
`evaluator_calls`. So the seed step is a real measurement at `evals_used = 0`,
and `evaluator_calls` excludes it while `sandbox_seconds` includes it. Both
behaviours are intentional; encode them, do not "fix" them.

**Probes are off-budget but not free.** A probe is subsampled, does not count
against the budget, and never updates best-so-far — its score is **not
comparable** to a full evaluation. But its wall time is real, and the ledger's
`sandbox_seconds` **omits it** (only `evaluate()` accumulates, `probe()` does
not). That is why `sandbox_seconds` is flagged `partial`; the true sandbox time
is the sum of `wall_s` over all steps.

**Note rows are not measurements.** A `note` step carries `best_so_far` as filler
in `combined_score`. Store `null` and set `is_measurement: false`, or the curve
grows flat segments that look like failed evaluations.

**`llm_calls` is derived, not metered.** It is back-computed at the end by
counting assistant messages in the agent history. Consequences: flag it
`derived`, and if `stop_reason == "harness_error"` the count was never taken —
write `null`, not `0`.

**Token fields are dead.** `llm_input_tokens` / `llm_output_tokens` exist in the
ledger and are serialised, but nothing in the codebase ever assigns them. They
are always `0`, which is **not** a measurement. Always write `null` +
`unmetered`. Any plot with tokens on the x-axis is currently impossible; say so
rather than plotting zeros.

**Invalid candidates vanish from rollout dirs.** A candidate that failed
validation has an entry in `round.json` but no `rollouts/` directory. Iterating
the filesystem instead of `round.json` silently drops its generation cost.

**Round numbers are not globally unique in meaning.** Campaigns get disjoint
20-wide round ranges per task (`fresh_all_launch.sh` assigns cp:310,
hadamard:330, … ahc058:510), and other drivers write into a shared `outer/`.
Identity is `(workspace, round, task, k, run_idx)` — never round alone.

**Two scales.** Store `combined_score` only. Raw paper-scale values (`c5`, `c1`,
`c2`, `sum_radii`, `det_ratio`, AHC sums) are derived on read from
`tasks.jsonl:raw_metric.to_combined`. `c5` and `c1` are **lower-is-better** raw;
their combined form inverts them. Mixing the two scales in one column is the
easiest way to publish a wrong table.

**Budgets differ across rows of the same table.** The hadamard `h2_initial`
reference is a 20-evaluation run; a separate 60-evaluation run for the same task
and harness exists. Different budget = different point on the compute axis, and
arguably a different method. Never merge them.
