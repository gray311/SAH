Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Strategy:

1. EDIT the seed program to change num_restarts and hyperparameters

2. Call evaluate_solution ONCE per candidate with different hyperparameters

3. Try num_restarts=3, base_learning_rate=0.01, num_steps=59000 first

4. If combined_score > 1.0, finish immediately

5. Explore different num_intervals (800->1600), different learning rates, different seed_start values

Key: The optimizer trains for 59000 steps. Generate diverse INITIALIZATIONS and let the optimizer do the work. Don't waste evals on analytic screening - train everything.
