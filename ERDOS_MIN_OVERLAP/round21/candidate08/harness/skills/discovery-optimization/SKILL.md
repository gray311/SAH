---
name: discovery-optimization
description: "Generate many diverse pattern-based initializations for Erdos optimization with\nprecomputed analytical scores (integral=1.0, c5_bound). Screen candidates before full eval."
---

# Candidate Generation and Screening Strategy

## Understanding the Problem
We need to find a step function h: [0,2] -> [0,1] that minimizes the maximum correlation
with its shifted versions. The seed optimizer trains for 120,000 steps per candidate - very expensive.

## Strategy: Generate Many, Screen Cheaply

1. CALL generate_candidates(num_candidates=12) to get 12 structurally diverse initializations.
   Patterns include: Golomb ruler, bipartite, tri-modal, various threshold patterns, random seeds.

2. ANALYZE each candidate:
   - Check integral: MUST be 1.0 (constraint). Skip if not.
   - Check c5_bound (precomputed analytical score). This tells us the objective value WITHOUT training.
   - Only proceed with evaluation if c5_bound < 0.370 (promising start)

3. For candidates with c5_bound < 0.370:
   - CALL evaluate_solution to get the true optimized score after 120k training steps.
   - Track the best combined_score seen.

4. If you've evaluated 3-5 candidates and none beat the seed score:
   - CALL generate_candidates again with different temperature (0.7 or 0.9).
   - Try to get different patterns.

5. Budget management:
   - You have ~30 evaluation budget total.
   - Each full evaluation costs 1 eval.
   - Use probe_solution to get approximate scores quickly for new candidates.

## Why This Works

- 12 diverse patterns give multiple chances to find a good starting point.
- Precomputed analytical scores let us screen without expensive training.
- Only promising candidates (c5_bound < 0.370) get full evaluation.
- Typical workflow: 12 candidates -> 2-5 pass screen -> 2-4 full evals -> 1-2 improvers.

## Example

Candidate 0 (Golomb): integral=1.000, c5=0.362 -> EVALUATE
Candidate 1 (Bipartite): integral=1.000, c5=0.371 -> SKIP (>=0.370)
Candidate 2 (Tri-modal): integral=1.000, c5=0.358 -> EVALUATE
Candidate 3 (Random1): integral=1.000, c5=0.385 -> SKIP
Candidate 4 (Random2): integral=1.000, c5=0.365 -> EVALUATE

Result: 3 evaluations used, best c5=0.362 -> combined_score = 0.3809/0.362 = 1.052
