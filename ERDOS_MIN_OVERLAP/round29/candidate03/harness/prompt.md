Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed program's initialization uses sigmoid(latent) which may distort good analytical patterns.
We need TWO PHASES:

PHASE 1: Generate diverse INITIAL PATTERNS using search_patterns (analytical c5 via FFT)

PHASE 2: For candidates with c5_bound < 0.375, use refine_candidate to ITERATIVELY IMPROVE them BEFORE full evaluation

STRATEGY:

1. CALL search_patterns(temperature=0.5) to get 5 diverse candidates with analytical c5_bound

2. SCREEN with probe_solution on each

3. For candidates with c5_bound < 0.375, CALL refine_candidate 2-3 times to sharpen peaks/remove noise

4. CALL evaluate_solution on the BEST refined candidate (lowest c5_bound after refinement)

5. If no improvement, try different patterns (bipartite-only, multi-peak-only) then repeat

CRITICAL: Never call evaluate_solution on a candidate without first refining it (unless it's already very low c5_bound)

BUDGET: 60 full evals, ~30 probes. Use probes for screening, refine cheaply, then evaluate once.
