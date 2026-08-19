Erdős minimum overlap (C₅) optimization task.

Current best known upper bound: C₅ ≤ 0.38092303510845016
Combined score = 0.38092303510845016 / c5_bound
Goal: Find c5_bound < 0.380923 (combined_score > 1.0)

SEED ANALYSIS:
- Seed optimizer uses 15 pattern-based initializations, each trained for 59000 steps
- Seed achieves c5_bound ≈ 0.381 (combined_score ≈ 1.0)
- The optimizer is gradient-based (implicit in JAX code)

SEARCH STRATEGY:
1. FIRST: Analyze what the seed optimizer does
   - Study the Hyperparameters: num_intervals=800, lr=0.0062, steps=59000, penalty=61.0
   - Understand the 15 pattern variations in _get_best_initialization
2. SECOND: Try systematic hyperparameter sweeps
   - Vary learning rate (0.001 to 0.1)
   - Vary num_steps (10000 to 100000)
   - Vary penalty_strength (10 to 200)
   - Vary num_intervals (200 to 2000)
3. THIRD: Modify the optimizer algorithm
   - Change optimization method (SGD variants, Adam, etc.)
   - Add constraint enforcement during optimization
   - Try different initialization strategies
4. FOURTH: Try entirely different approaches
   - Optimize pattern parameters directly (not latent)
   - Use multiple restarts with different strategies
   - Try spectral methods or other techniques

EVALUATION DISCIPLINE:
- Each edit MUST be tested with evaluate_solution
- Before submitting a candidate, ensure it compiles and runs
- If multiple edits look similar, pick the most promising
- Use probe_solution ONLY if available (approximate eval)

BUDGET: 30 evals total. Expect to need ~5-10 evals per promising direction.

NEVER waste evals on:
- Candidates that are parameter-similar to seed
- Edits that don't change the optimizer meaningfully

REPORT: When you find combined_score > 1.0, call finish with summary.
