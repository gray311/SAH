Erdos C5 Optimization: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly.
h values in [0,1].

Current best: C5 <= 0.38092303510845016.
GOAL: Find h achieving c5_bound < 0.38092303510845016.

STRATEGY:
1. CALL generate_initial_step_function to create valid h with integral=1
2. Use generate_correlation_profile to find problematic shifts
3. Modify h at those shifts using localized edits
4. Use probe_solution to screen candidates (c5_bound < 0.375)

KEY: Start with VALID initializations. Use generate_initial_step_function.
