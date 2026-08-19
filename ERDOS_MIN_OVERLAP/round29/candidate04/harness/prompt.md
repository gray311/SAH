Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The optimal solution is likely a SIMPLE STEP FUNCTION (constant on intervals), not a smooth sigmoid.
The seed program's gradient-based optimization gets stuck because it starts from smooth initializations.

STRATEGY:
1. FIRST, USE discrete_step_search to generate step functions with 2-10 intervals (TRUE step functions, not smooth)
2. Each step function has a fixed shape (e.g., "up" step, "down" step, "up-down" step)
3. CALL probe_solution on each to get approximate C5 bounds
4. CALL evaluate_solution on the BEST 1-2 candidates (those with c5_bound < 0.375)
5. If no success, THEN try the seed's gradient optimization with different seeds

EVALUATE ONLY when c5_bound < 0.375 (combined_score > 1.01)
Use discrete_step_search to get true step functions, not smooth sigmoids.
