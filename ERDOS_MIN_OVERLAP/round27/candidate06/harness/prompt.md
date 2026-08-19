Erdos minimum overlap (C5): Minimize max_k integral h(x)(1-h(x+k))dx for h:[0,2]->[0,1] with integral(h)=1.

SEED SCORE: 0.999945. Current best C5 <= 0.380923.

DIAGNOSIS: Seed tests 15 hardcoded patterns + gradient descent. Hyperparameter tuning WON'T help.

BREAKTHROUGH: INJECT NEW PATTERNS 15+. Tool inject_patterns inserts new pattern definitions into
_get_best_initialization() AFTER pattern 14.

WORKFLOW:
1. CALL inject_patterns() - adds patterns 15-17 (asymmetric bipartite, multi-scale peaks, fractional waves)
2. CALL evaluate_solution on injected code
3. If no improvement, repeat inject_patterns 2-3 times
4. Skip analytical-screening and generate_ready_candidates - red herrings
5. Only use edit_solution if injection fails

KEY: c5_bound < 0.380923 requires NEW COMBINATORIAL PATTERNS, not hyperparameter tuning.
