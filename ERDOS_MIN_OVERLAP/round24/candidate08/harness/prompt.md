Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

### SEARCH STRATEGY - ANALYTICAL INITIALIZATION FIRST

1. START by calling generate_ready_candidates(temperature=0.5) to get 3 integral-constrained candidates
2. EXAMINE each candidate's c5_bound - these are precomputed via FFT, no training needed
3. CALL evaluate_solution ONLY on candidates with c5_bound < 0.375 (probe did the filtering)
4. If NO candidate beats current best, TRIPLE the diversity: call generate_ready_candidates(temperature=0.8)
5. If STILL no improvement, try temperature=1.0 for more exploration
6. Do NOT waste evals on hyperparameter tuning of the seed optimizer - the issue is initialization, not training

### Why this works

- generate_ready_candidates creates valid step functions with exact integral=1
- c5_bound computed analytically in O(N log N) via FFT (instant)
- We screen hundreds of candidates for FREE before spending any eval budget
- Once we find c5_bound < 0.375, we have a 70% chance of beating current best

### Pattern guidelines

Golomb ruler patterns (5-7 marks at optimal spacing) minimize overlap by spreading mass.
Tri-modal patterns (3 narrow peaks) concentrate mass at strategic locations.
Bipartite patterns (threshold functions) provide simple baselines.

All patterns should be normalized to integral=1 before evaluation.

USE probe_solution sparingly - it is approximate and unreliable for this problem.
Rely on generate_ready_candidates for cheap, exact filtering.
