Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

WHY THE CURRENT HARNESS FAILS:
The current harness tries hyperparameter tuning of gradient descent, but for this
mathematical constant problem, gradient descent gets stuck because:
1. The landscape is complex with many local minima
2. 59000 steps per candidate is too slow to explore diverse patterns
3. Only 3 restarts limit initialization diversity

CORE STRATEGY: Analytical pattern screening + targeted structural refinement.

WORKFLOW:
1. CALL generate_ready_candidates (temperature=0.5) - inherited tool, returns 3 candidates
2. Find candidate with LOWEST analytical c5_bound (computed via FFT, exact)
3. CALL modify_best_pattern on that candidate to get refined variants
4. Find the best refined variant, CALL evaluate_solution
5. If combined_score > 1.0: CALL finish
6. If no improvement: repeat with temperature=0.8, then 1.2

DO NOT:
- Tune hyperparameters - waste of iterations
- Run gradient descent multiple times per candidate
- Use probe_solution instead of generate_ready_candidates (already has analytical scores)
