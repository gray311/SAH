Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. Call compact_analysis ONCE to get a lightweight summary of current best's correlation structure

2. Use simple_targeted_mutations to create 3 diverse mutations focusing on reducing overlap

3. Call probe_solution on each to quickly screen (target c5_bound < 0.385)

4. Evaluate the best 1-2 candidates fully

5. If no improvement, try different mutation types: spread_peaks, bipartite, localized

KEY: Keep outputs short to fit token budget. Only call analysis once. Focus on diversity.
