Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Strategy:
1. CALL compute_analytical_c5(h_array) ON your proposed h to get exact precomputed c5_bound
2. CALL compute_analytical_c5 ON the seed optimizer's best_initialization patterns (Golomb, bipartite, tri-modal)
3. Only CALL evaluate_solution on candidates where c5_bound < 0.37 (use 5-7 marks for Golomb)
4. If no improvement after 3 evaluations, TRY DIFFERENT PATTERNS: asymmetric bipartite (a=0.4, 0.45, 0.5), 5-peak patterns

Key: The seed's _get_best_initialization uses 15 patterns. You must call compute_analytical_c5 to screen ALL of them before evaluating.
