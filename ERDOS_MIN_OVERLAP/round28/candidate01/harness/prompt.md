Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The optimizer needs DIVERSE INITIAL CONFIGURATIONS, not just hyperparameter tuning.

STRATEGY:
1. FIRST, USE search_patterns TO GENERATE 5-10 DIVERSE INITIAL STEP FUNCTIONS (Golomb, bipartite, triangular, etc.)
2. CALL probe_solution on each to get approximate C5 bounds (cheap, separate budget)
3. CALL evaluate_solution on the BEST 2-3 candidates (those with c5_bound < 0.375)
4. If no success, THEN vary hyperparameters of the training loop (num_intervals, learning_rate, penalty_strength)
5. NEVER waste evals on random latents - always use structured patterns first

EVALUATE ONLY when c5_bound < 0.375 (combined_score > 1.01)
Use search_patterns to get diverse, integral-constrained initializations in one call.
