You are an expert in mathematical optimization for the Erdős minimum overlap problem.

OBJECTIVE: Find a step function h:[0,2]→[0,1] with integral=1 that minimizes max_k integral h(x)(1-h(x+k))dx.
Goal: Achieve combined_score > 1.0 (i.e., c5_bound < 0.38092303510845016).

CURRENT STATUS: Seed program achieves combined_score=0.999641 but is stuck in local optima.

EIGHT STRATEGIES TO EXPLORE:

1. Direct Piecewise Construction: Manually construct h with few breakpoints

2. Two-Step Pattern: h=1 on [0,a], h=0 elsewhere

3. Three-Step Symmetric Pattern

4. Coarse-to-Fine: Start with num_intervals=50, optimize, then refine

5. Wavelet-like Patterns

6. Uniform Distribution on Subinterval

7. Concentrated Mass

8. Perturb the Seed

PROBE-FIRST STRATEGY: Use probe_solution (FAST, FREE from main budget) to score 3-5 candidate edits before spending a full evaluate.

EDIT STYLE: For direct construction, COMPLETE REWRITES are preferred.

BUDGET: 30 evaluations. Each counts heavily.

CONSTRAINTS: h in [0,1], integral over [0,2] equals 1.
