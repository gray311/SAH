---
name: exploration-loop-strategy
description: A systematic exploration strategy for constrained evaluation budgets. Guides generating, ranking, and selecting variants using probe_solution.
---

# Exploration Loop for Limited Evaluation Budget

## The Strategy
With only ~20 evaluations, use probes:
- 1 evaluate_solution call → rank 3-5 variants → explore 3-5 effectively
- Test 40-60 hypotheses with 20 evals

## Step-by-Step
1. **INITIALIZE**: Probe the seed (baseline)
2. **VARIANT GENERATION**: Create 3 SEARCH/REPLACE edits (parameter tweak, different algorithm, structural improvement)
3. **PROBE RANKING**: Call probe_solution on each variant → rank them
4. **FULL EVALUATION**: Call evaluate_solution on top 2 variants → keep best
5. **REPEAT** (while evaluations_left > 5):
   Generate new variants around current best → Probe all → Evaluate top 2
6. **CONVERGE**: When no improvement after 3 cycles, call finish

## Decision Rules
- Probe scores diverge: trust probe, full-eval the winner
- Probe scores similar: full-eval both
- Probe crashes: check validity, fix code
- Validity=0 after full-eval: fix error, retry with corrected code

## Example Session Flow
Probe seed → Rank = 1.0
Gen 3 variants → Probe all → Variants A,B,C rank 0.95, 0.92, 0.88
Evaluate A,B → A wins, B discarded
Gen 3 variants around A → Probe → Rank A-mod1=0.98, A-mod2=0.97, A-mod3=0.94
Evaluate A-mod1 → 1.03 (best)
... (repeat) ...
Finish with score 1.03
"
