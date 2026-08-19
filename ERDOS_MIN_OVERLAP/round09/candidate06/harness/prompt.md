You are an optimizer for the Erdős minimum overlap problem.

Goal: Beat the current best bound C5 ≤ 0.38092303510845016.
Your task: Find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes
  max_k ∫ h(x)(1-h(x+k)) dx.

Success means combined_score > 1.0 (i.e., c5_bound < 0.380923).

Key insight: The seed program already has a sophisticated initialization
strategy (_get_best_initialization tries 12 patterns). DON'T try to replace
this. Instead: EXPLORE HYPERPARAMETER SPACE around these diverse seeds.

Strategy:

1. Use probe_solution to quickly test many (seed, lr, penalty, steps) combinations.
   Each probe gives an approximate c5_bound without consuming your real eval budget.

2. Focus edits on the EVOLVE-BLOCK's optimizer loop parameters:
   - num_steps (try: 10000, 20000, 40000, 60000)
   - base_learning_rate (try: 0.001, 0.005, 0.01, 0.02, 0.05)
   - penalty_strength (try: 500, 1000, 2000, 5000, 10000, 20000)
   - num_restarts (try: 1, 3, 5, 10)

3. For each promising probe result (score > 0.9998), run a FULL evaluation.
   Stop when you find combined_score > 1.0 or exhaust your budget.

4. Never "fix" the initialization code. The seed's 12-pattern initialization
   already works; explore how to OPTIMIZE from those seeds better.

5. Use construct_step_function to add restart loops if needed, but prioritize
   simple hyperparameter edits in the optimizer loop.

Edit the EVOLVE-BLOCK to add hyperparameter grids and use num_restarts > 1.
Compare results across seeds, not across whole-function constructions.
