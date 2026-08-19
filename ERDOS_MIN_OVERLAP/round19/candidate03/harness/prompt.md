Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).

Strategy:

1. EDIT the EVOLVE-BLOCK to modify hyperparameters in Hyperparameters class

2. Key parameters to explore:
   - num_intervals: 400, 500, 600, 800, 1000 (finer resolution)
   - base_learning_rate: 0.003, 0.005, 0.0062, 0.01, 0.02
   - num_steps: 30000, 45000, 59000, 75000
   - penalty_strength: 30, 50, 61, 100, 150
   - num_restarts: 5, 7, 10 (more restarts for better coverage)

3. Call evaluate_solution after each edit

4. Use probe_solution to screen before full evaluation if available

5. Make ONE focused edit at a time (one parameter per edit)

6. Only use tools: edit_solution, evaluate_solution, probe_solution, finish

7. If code is invalid, try a different edit

8. Stop when combined_score > 1.0
