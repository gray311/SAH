Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

CRITICAL: Use train_and_probe_batch to explore many trained candidates efficiently.

Strategy:

1. CALL train_and_probe_batch ONCE at the start (tests all 15 seed patterns with 3 restarts each)

2. The tool returns trained candidates with their c5_bound estimates

3. CALL evaluate_solution ONLY on candidates where c5_bound < 0.3809 AND you have budget

4. If none pass, CALL train_and_probe_batch again with modified hyperparameters

5. Never waste evals on candidates with c5_bound >= current best

Key: The seed optimizer trains for 59000 steps. Use it to find better initializations, then validate with evaluate_solution.
