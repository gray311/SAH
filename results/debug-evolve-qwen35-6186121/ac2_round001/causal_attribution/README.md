# AC2 trajectory causal-attribution audit

## cand01: prompt-only candidate

The materialized H2 changes only `system_prompt`; it adds guidance about step
functions, piecewise-constant initialization, multi-scale refinement, sparsity,
learning rate, and symmetry. It does **not** propose a Gaussian tail.

The executor's first edit uses
`exp(-arange(N) / N * 0.5)`, which is exponential decay rather than a step.
Its second edit combines a 70% hard step with
`exp(-arange(N) / N * 2.0)`. The trajectory calls the latter
"Gaussian-like", but mathematically it is also exponential decay. The public
task already names Gaussian, exponential-decay, and step families, so neither
the step prior nor the tail can be uniquely sourced to cand01 by lexical
inspection.

The same-seed parent control independently states that the public task's key
insight is the step-function result and makes a step-like first edit without
seeing cand01. That attempt scores `0.604173`; it then switches to a triangular
initialization and reaches `0.978144`. This is direct trajectory evidence that
the step family was already available to the base executor, while the exact
hard-step-plus-exponential-tail realization remains specific to the candidate
sample.

### Same-seed parent control

The retrospective control uses the incoming parent H2 with the exact same task,
seed program and registry hashes, two-evaluation budget, frozen model, and
decode seed `200001`.

| quantity | score / delta |
|---|---:|
| seed program | 0.954826984197 |
| parent H2 control | 0.978144482070 |
| cand01 H2 | 0.980520432265 |
| cand01 gross gain over seed | +0.025693448068 |
| parent gain over seed | +0.023317497873 |
| paired cand01 effect | **+0.002375950195** |
| paired effect / gross gain | **9.25%** |

Conclusion: cand01 changed the rollout outcome under this common decode seed,
but only a small fraction of its gross improvement is attributable to the
harness. About 90.75% of the observed gain was already produced by the parent
H2/executor route. The exact tail idea is not an explicitly proposed strategy,
so it must not be reported as direct strategy enactment. A single pair estimates
the total prompt effect, not which sentence mediated it; multiple matched seeds
are required for stable training credit.

Source artifact: `../paired_replay_cand01/paired_effect.json`.

## cand03: generated skill and budget-state bug

The original rollout mounted `c2-optimization`, but the executor loaded only
`discovery-optimization`. The skill was callable; the candidate prompt both
duplicated much of its advice and inherited a stale optional-skill instruction,
so the executor bypassed it. This was executor policy under a contradictory
prompt, not a NexAU registry/materialization failure.

The patched runtime now injects every mounted generated `SKILL.md` in full
before the first edit and records the delivery separately from model-chosen
`LoadSkill` calls. The end-to-end replay shows:

- `loads = 0`, `tool_loads = 0` — the executor did not choose to load it;
- `runtime_injections = 1`, `loads_before_first_edit = 1` — the complete skill
  was nevertheless deterministically enacted;
- `score_eligible = true`;
- exactly two evaluator calls and two staged edits;
- no unvalidated post-budget edit;
- best score `0.995632863092`.

Source artifact: `../patched_replay_cand03/enactment_budget_audit.json`.

## Training policy after the fix

1. Every active generated skill is deterministically delivered on every
   rollout, including after it becomes inherited. The lineage separately marks
   skills added/updated by the current H1 proposal.
2. Every candidate H2 is evaluated against its incoming parent H2 on matched
   decode seeds. The collector verifies task, model, seed-program hashes,
   registry hash, evaluation budget, decode seed, both the declared candidate
   and parent H2 hashes, and package stability before assigning credit.
3. Proposer reward is the mean matched effect
   `candidate_score - parent_control_score`, gap-normalized for the task. The
   candidate's absolute score remains diagnostic and program-incumbent state is
   tracked separately.
4. `reward.paired_repeats` controls common-random-number repeats. One repeat is
   supported for smoke tests; use at least three for training campaigns.
5. Strategy-origin labels remain diagnostic. They cannot replace a
   counterfactual because an autoregressive prompt change may indirectly alter
   downstream ideas that were not stated verbatim.

The runnable campaign template is
`code/SAH/config/examples/ac2_paired.yaml`.
