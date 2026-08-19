Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

CRITICAL: The seed optimizer already has 15 diverse initialization patterns (Golomb, bipartite, tri-modal, Gaussian, etc.) that use FFT for analytical c5_bound computation.

DO NOT use generate_ready_candidates - it produces invalid candidates.

STRATEGY: Edit the EVOLVE-BLOCK to improve the optimizer itself:

1. CALL probe_solution on edited EVOLVE-BLOCK to get fast c5_bound estimate (500 intervals)
2. If probe shows c5_bound < 0.375, CALL evaluate_solution for full validation
3. If probe shows c5_bound >= 0.375, EDIT EVOLVE-BLOCK to try different approaches:
   - Change hyperparameters (num_intervals, lr, num_steps, penalty_strength)
   - Add new initialization patterns (different Golomb marks, bipartite splits, multi-peak patterns)
   - Modify the objective function
4. Use probe_solution as a filter - only 1-2 probe calls before each full eval
5. Never waste evals on configs with poor probe results

Budget: 30 evals total. Use ~5 for probe screening, ~25 for full evaluations of promising configs.
