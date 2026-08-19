Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
KEY INSIGHT: The seed program has 14+ fixed patterns, but we need to systematically explore NEW architectural choices for step functions (number of steps, step locations, and their values), not just vary hyperparameters.
STRATEGY:
1. FIRST, USE construct_step_function to build step functions with controlled architecture (specify num_steps, step locations, and values)
2. CALL probe_solution on each to get approximate C5 bounds
3. CALL evaluate_solution on the BEST 2-3 candidates (those with c5_bound < 0.375)
4. If no success, THEN vary hyperparameters of the training loop
5. NEVER waste evals on random latents - always use structured construction first
EVALUATE ONLY when c5_bound < 0.375 (combined_score > 1.01)
Use construct_step_function to get architecturally-controlled initializations in one call.
