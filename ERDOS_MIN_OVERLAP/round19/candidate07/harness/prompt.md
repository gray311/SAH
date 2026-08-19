Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).

CRITICAL STRATEGY - HYPERPARAMETER TUNING:

1. DO NOT generate many new patterns. The seed's 15 patterns are proven to work.

2. For EACH iteration, call edit_solution to change ONE hyperparameter in the EVOLVE-BLOCK:
   - num_intervals: try values from [400, 800, 1200, 1600, 2000]
   - base_learning_rate: try values from [0.001, 0.005, 0.01, 0.02, 0.05]
   - penalty_strength: try values from [10.0, 30.0, 50.0, 80.0, 100.0]
   - num_steps: try values from [30000, 59000, 90000, 120000]
   - num_restarts: set to 1 or 2 (save budget)

3. After editing, CALL evaluate_solution ONCE to measure improvement.

4. Use systematic grid search: change one parameter at a time, keep the best result.

5. Budget: 30 evaluations total. Use ~2-3 evals per iteration, run 10-12 iterations.

6. Focus on fine-tuning the seed's existing patterns - small hyperparameter changes can yield big improvements.

7. Never waste evals on completely new pattern generations.

Key: The seed optimizer already finds good solutions. We need to TUNE it better.
