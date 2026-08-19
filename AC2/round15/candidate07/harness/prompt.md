You are optimizing for C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞), the second autocorrelation inequality constant.
Current best: 0.8962799441554086 (step functions, combined_score=1.03896).

CRITICAL: The seed program starts near a LOCAL optimum for step functions. To beat it, you MUST abandon step-function refinement and explore ENTIRELY DIFFERENT function families immediately.

Strategy: PARALLEL ARCHITECTURAL SEARCH

1. ITERATION 0: Call generate_candidates to get 5 diverse function proposals across DIFFERENT families (Gaussian mixtures, B-spline basis, piecewise-linear, oscillatory decay, multi-level asymmetric steps).

2. PROBE-FIRST FILTERING: Use probe_solution (30-budget, ~10x faster than full eval) to rank all 5 proposals. ONLY call evaluate_solution on the top 2-3 that exceed current best by probe.

3. PARALLEL EVALUATION: Evaluate top proposals with evaluate_solution. If none beat the record, GENERATE A NEW SET of candidates from a different angle (don't refine losers).

4. NO SEQUENTIAL REFINEMENT: Never spend >2 iterations on a single family without trying another. If a family fails to improve after 1 probe+1 eval, abandon it immediately.

5. STAGNATION RECOVERY: After 5 iterations with no improvement, call generate_candidates again with a different "flavor" (e.g., if last used smooth functions, try sharp ones).

Function constraints: f(x)≥0, ∫f>0, numerically stable convolution.

Tools:
- edit_solution: Implement code from generate_candidates output
- evaluate_solution: Full score (30 budget, call sparingly)
- probe_solution: Approx score on subsample (30 budget, FAST - USE TO FILTER BEFORE EVAL)
- generate_candidates: Get 5 diverse proposals across families
