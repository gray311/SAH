Erdos minimum overlap problem (C5): Find a step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY: Build step functions directly from combinatorial constructions, not continuous optimization.

PHASE 1: Generate step functions from templates:
- Uniform partition (equal-width steps)
- Bipartite (single threshold at a)
- Tripartite (two thresholds at a, b)
- Golomb ruler-like (discrete marks)
- Peak patterns (n narrow peaks)

PHASE 2: For each candidate, call probe_solution to screen (cheap, 500 intervals).
Keep only those with c5_bound < 0.382.

PHASE 3: Call evaluate_solution on the best 1-2 probe-selected candidates.
If combined_score > 1.0, finish.

KEY INSIGHT: Continuous latent optimization is too slow. Build step functions directly from known good combinatorial patterns.

BUDGET: 60 full evals, ~30 probes. Use probes to screen many candidates quickly.
