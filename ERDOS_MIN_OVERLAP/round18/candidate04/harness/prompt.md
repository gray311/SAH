Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016 (combined_score > 1 means improvement).

CRITICAL: The seed optimizer trains for 59000 steps and uses sophisticated patterns.

STRATEGY:

1. EDIT hyperparameters or add new patterns to _get_best_initialization

2. CALL evaluate_solution ONCE per edited candidate (it runs the full optimizer)

3. Test 1-3 variations, pick the best. If combined_score > 1, call finish.

Key: Run the actual optimizer. Do NOT skip it with fake candidates.
