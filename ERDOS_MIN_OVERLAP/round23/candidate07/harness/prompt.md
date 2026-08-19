Erdos minimum overlap: find h:[0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h)=1 exactly. Current best: C5<=0.38092303510845016.

STRATEGY (CRITICAL):

1. EDIT the seed optimizer to vary num_restarts (1, 2, 3) and seed_start (0, 1, 2, 3) to get 3-4 diverse candidates

2. For each candidate, call probe_solution FIRST (cheap 500-interval eval) to get quick c5 estimate

3. If probe c5 < 0.37 AND integral ~ 1.0, call evaluate_solution for full 800-interval score

4. If any full eval gives c5 < 0.38092303510845016 (combined_score > 1.0), call finish()

5. If no improvement after 3 iterations, EDIT to try different random seeds or Golomb ruler initialization

Key: The seed optimizer trains 59000 steps per candidate. Use probe_solution to filter, not evaluate_solution.

Template edits: Change num_restarts and seed_start in EVOLVE-BLOCK. Use num_restarts=3, seed_start=0 for baseline. Then try num_restarts=1, seed_start=1,2,3 individually.
