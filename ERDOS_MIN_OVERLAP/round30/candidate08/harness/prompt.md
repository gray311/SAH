Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY (CRITICAL):

1. FIRST: CALL search_patterns(temperature=0.5) to generate 5 diverse initial step functions.
   Each has precomputed c5_bound via FFT (no training, instant).

2. IDENTIFY the BEST pattern candidate (lowest c5_bound).

3. CALL mutate_best_pattern with the best candidate. This applies targeted mutations
   (adjust peak widths, shift centers, modify amplitudes) to create variants.
   Each mutated variant has precomputed c5_bound via FFT.

4. SCREEN all mutated variants with probe_solution (cheap, separate budget).

5. CALL evaluate_solution on the TOP 1-2 mutated candidates with c5_bound < 0.375.

6. If no improvement after 2 rounds of pattern->mutate->evaluate, call search_patterns with temperature=0.8.

7. NEVER call evaluate_solution on c5_bound > 0.375.

KEY INSIGHT: The seed optimizer gets stuck. We need to GENERATE diverse patterns, then MUTATE the best ones
using domain-specific operations (peak shifting, width adjustment) to escape local optima.

TOOL USAGE ORDER: search_patterns -> mutate_best_pattern -> probe_solution -> evaluate_solution (only best candidates)
