Erdos minimum overlap (C5): Find h: [0,2]->[0,1] step function minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINTS: integral(h)=1 exactly; h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.00001).
GOAL: Find h with combined_score > 1.0.

STRATEGY: Diversity-first search with constraint satisfaction.

1. Generate diverse step function candidates using generate_candidates (at least 5-7 different structural types).
2. Ensure each candidate satisfies: values in [0,1] and integral = 1 (use sigmoid + scaling).
3. Call probe_solution on each candidate to screen for c5_bound < 0.381.
4. Call evaluate_solution on the 2-3 best probe candidates.
5. If no improvement after 2-3 rounds, try different candidate generation strategies.

KEY: The seed program uses 800 intervals with sigmoid activation. Your mutations must preserve the program structure but change the h array values to create valid step functions with integral=1.
