Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. Generate structured step functions using step_function_generator with different patterns:
   - bipartite: single threshold at various positions
   - multi_peak: 2-4 narrow peaks with equal mass
   - golomb: sparse marks at positions minimizing overlap

2. Ensure integral(h) = 1 by normalizing the step heights

3. Call probe_solution on generated candidates to filter c5_bound < 0.378

4. Evaluate top candidates fully

5. If no improvement, try varying the number of intervals (100-2000)

KEY INSIGHT: The seed's random latent initialization doesn't produce good step functions.
Try discrete combinatorial structures instead.
