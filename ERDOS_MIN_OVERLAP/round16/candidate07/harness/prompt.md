You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016
Goal: Find combined_score > 1.0 (c5_bound < 0.380923)

KEY INSIGHT: The seed program already uses 12 diverse initialization patterns.
The bottleneck is NOT initialization diversity - it's HYPERPARAMETER OPTIMIZATION.

The seed's _get_best_initialization tries 12 patterns and picks the best latent.
With num_restarts=3, it already explores diversity. Setting num_restarts=1 WASTES this.

STRATEGY: Systematic hyperparameter search

Steps:
1. VARY hyperparameters systematically:
   - num_intervals: try [200, 400, 800, 1600] (coarser first for speed)
   - penalty_strength: try [10, 30, 61, 100, 200] (find optimal constraint penalty)
   - base_learning_rate: try [0.001, 0.005, 0.01, 0.02]
   - num_steps: try [10000, 25000, 59000, 100000]

2. For each hyperparameter combo:
   - EDIT to set the hyperparameters
   - Keep num_restarts=3 (use the seed's built-in diversity)
   - Call probe_solution to check c5_bound estimate and constraint satisfaction
   - Skip full eval if probe shows c5_bound >= 0.375 or constraint violation

3. Call evaluate_solution on top 3-5 hyperparameter combinations with c5_bound < 0.36

4. If no improvement, try further hyperparameter refinement or modify _get_best_initialization

Key insight: Use the seed's 12 initialization patterns! Don't set num_restarts=1.
The FFT evaluator is fast - use probe_budget to screen 20+ hyperparameter combos.
