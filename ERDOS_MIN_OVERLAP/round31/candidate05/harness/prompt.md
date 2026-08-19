Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. Use the mutation_generator tool to create concrete candidate functions:
   - Try "bipartite" for single threshold: h(x) = 1 if x < t else 0
   - Try "multi_modal" for 2-3 peaks at specific locations
   - Try "spread_peaks" for many narrow peaks

2. For each mutation, check: integral(h) = 1, h in [0,1]

3. Call probe_solution on candidates to screen (c5_bound < 0.382)

4. Call evaluate_solution on best probe candidates (c5_bound < 0.380)

5. If no improvement, try different mutation types

KEY: Use concrete mutations, not random hyperparameter tuning.
