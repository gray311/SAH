You are an expert in combinatorial optimization and constructive algorithms.

**OBJECTIVE**: Find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes
c5_bound = max_k ∫ h(x)(1-h(x+k)) dx. Target: c5_bound < 0.38092303510845016.

**KEY INSIGHT**: The seed's gradient-based approach fails because the objective is
non-convex and the integral constraint creates hard boundaries. Use **direct
construction** instead of latent-space optimization.

**STRATEGY**: 
1. Start with simple explicit piecewise constant functions (1-5 breakpoints)
2. Use local search: swap breakpoints, adjust widths, optimize values under [0,1]
3. Try structured patterns: uniform blocks, alternating patterns, centered mass
4. Verify constraints: integral must be exactly 1, values in [0,1]

**EDITS**: Completely rewrite the EVOLVE-BLOCK to use explicit construction and
local search. Replace the Adam optimizer approach with constructive search.

**BUDGET**: 30 evaluations. Each edit should be a complete, runnable program.
