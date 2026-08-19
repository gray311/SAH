You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

Strategy: The seed program has a sophisticated multi-restart optimizer with 12 initialization
patterns. Your job is NOT to replace this, but to systematically TUNE its hyperparameters.

Steps:
1. First, CALL evaluate_solution on the seed to establish baseline
2. EDIT the EVOLVE-BLOCK to change ONE hyperparameter at a time:
   - num_intervals: try 400, 800, 1600, 3200 (coarser/finer discretization)
   - base_learning_rate: try 0.001, 0.005, 0.01, 0.02
   - penalty_strength: try 100, 500, 1000, 5000, 10000
   - num_steps: try 20000, 50000, 80000, 100000
   - num_restarts: try 1, 3, 5, 10
3. For each hyperparameter variant, use probe_solution to quickly screen (if probe fails constraint, skip)
4. Call evaluate_solution on the top 2-3 promising variants
5. If none improve, try editing _get_best_initialization() to add NEW patterns
6. Keep the best program and continue iterating

Focus: Hyperparameter sweep FIRST, then initialization pattern expansion.
