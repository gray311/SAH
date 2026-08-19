Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 1.00001 (c5_bound < 0.380923).

KEY INSIGHT: The seed program uses only 3 restarts. This is TOO FEW to escape local optima.

STRATEGY:

1. EDIT the seed program's num_restarts from 3 to 15 (or higher). More restarts = better chance of finding good baselines.

2. Keep num_intervals=800 (higher resolution is important for accurate c5 computation).

3. Keep penalty_strength=61 (strong constraint enforcement needed).

4. After editing, CALL evaluate_solution to test the improved restart count.

5. If no improvement, try even higher restart counts (20, 30, 50).

6. Budget: Use evals to explore restart counts: 15, 25, 40, 50, 75, 100.
