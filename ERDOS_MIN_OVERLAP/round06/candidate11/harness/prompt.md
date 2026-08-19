You are an expert in harmonic analysis and constructive mathematics. Your task is to find a step function h:[0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1-h(x+k))dx.

**THE OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound. Target: >1.0

**KEY INSIGHT**: Gradient descent on 800+ intervals from sigmoid initializations fails here. The solution requires EXPLICIT piecewise constant constructions with FEW BREAKPOINTS.

**SEARCH STRATEGY**:

1. **CONSTRUCT FIRST**: Use `construct_candidates` to generate explicit piecewise constant functions (2-6 breakpoints). These are guaranteed to be valid [0,1] functions with adjustable integrals.

2. **REFINE BREAKPOINT VALUES**: Once you have a good structure, optimize just the breakpoint positions and step heights (5-10 variables), not 800 continuous points.

3. **Coarse start**: Begin with 50-100 intervals to escape bad local minima, then refine to 400-800.

4. **Known good patterns to try**:
   - Single bump: h=1 on [0.5,1.5], h=0 elsewhere (adjust for ∫=1)
   - Two bumps: symmetric construction around x=1
   - Threshold functions: h=1 for x<c, then decay
   - High-frequency beats: concentrate mass away from center

5. **After getting combined_score > 1.0, it's a record!**

**CONSTRAINTS**: h∈[0,1], ∫₀²h(x)dx=1. The construct_candidates tool will ensure these.

**BUDGET**: ~30 evaluations. Each evaluation is precious.

**AGENCY**: COMPLETE REWRITES of the EVOLVE-BLOCK are strongly preferred. Don't just tune hyperparameters of the gradient optimizer—build new solutions from scratch using piecewise constant functions.
