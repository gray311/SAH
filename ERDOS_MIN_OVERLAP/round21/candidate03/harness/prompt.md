Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1 exactly.
Current best: C5 <= 0.38092303510845016.
Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).
Strategy:
CRITICAL: The seed optimizer is FAILING because it uses num_intervals=800 (too many intervals) and penalty_strength=61 (too high). This makes the optimization extremely slow and hard to satisfy constraints.
1. EDIT to REDUCE num_intervals to 100-200 (faster evaluation, coarser discretization).
2. EDIT to REDUCE penalty_strength to 5-20 (easier constraint satisfaction).
3. EDIT to INCREASE num_steps to 200000-500000 (more iterations for coarse grids).
4. Use seed's pattern variations but with the NEW hyperparameters.
5. Call generate_candidates(3) with the edited hyperparameters, then evaluate_solution on each.
6. Iterate: if no improvement, try different hyperparameter combinations (intervals=[100,150,200], penalty=[5,10,15,20], steps=[200000,300000,500000]).
7. Budget: Use all 30 evals to exhaust the hyperparameter grid.
