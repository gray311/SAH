Task: Find step function h: [0,2]->[0,1] minimizing max_k ∫ h(x)(1-h(x+k)) dx.

Current best upper bound: C5 <= 0.38092303510845016 (combined_score = 1.00001).
Goal: Beat this bound with combined_score > 1.0.

Constraints:
- h(x) must be in [0,1]
- integral(h) = 1.0 exactly

Strategy:

1. The seed optimizer uses num_intervals=800, penalty_strength=61.0, num_steps=120000.
   Keep these settings - they're optimized for accuracy. Do NOT reduce intervals.

2. Use the tool generate_candidates to produce valid initializations
   with precomputed integral=1.0 and analytical c5_bound scores.

3. CALL generate_candidates(num_candidates=12) to get 12 diverse patterns.

4. EXAMINE the 12 candidates:
   - Skip any with integral != 1.0 (constraint violation)
   - Skip any with c5_bound >= 0.370 (too bad to waste evals)
   - Call evaluate_solution on candidates with c5_bound < 0.370

5. If no improvement after 3 evals, CALL generate_candidates again with different temperature.

6. Use probe_solution to quickly rank new candidates before full evaluation.

7. EDIT the EVOLVE-BLOCK to set num_candidates=12 in generate_candidates call.

8. The optimizer trains for 120k steps - each full evaluation is expensive (~5 mins).
   Use probe (cheap) to screen, then evaluate (expensive) only on best candidates.
