You are an expert in constructing step functions for the Erdős minimum overlap problem.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
where c5_bound is the maximum overlap integral. Target: c5_bound < 0.38092303510845016.

**CONSTRAINTS**: h: [0,2] → [0,1], ∫h = 1 over [0,2].

**WINNING STRATEGY**: Don't use gradient descent on 800-point discretizations. Instead:

1. **Coarse construction**: Start with num_intervals=50, construct explicit piecewise constant functions
2. **Explicit restart classes**: Try different structural patterns:
   - Concentrated mass: h=1 on [0,1], h=0 elsewhere (adjust for constraints)
   - Symmetric blocks: h constant on [0,a], [b,2] for various a,b
   - Multi-block patterns: h on [0,x1], [x2,x3], [x4,2] with different heights
   - Sine-wave approximations: h(x) ≈ 0.5 + 0.5*sin(π(x-1)) + noise
3. **Iterative refinement**: Once you find a decent pattern with 50 intervals, refine to 200, then 800
4. **Budget discipline**: With ~30 evals, try 5-8 different structural classes, not 30 small tweaks

**EDIT GUIDANCE**: Complete rewrites of the EVOLVE-BLOCK are needed. Replace the Adam optimizer with explicit construction and optimization over breakpoint positions/values.

**AGENCY**: You can completely redesign the optimizer class. Try evolutionary search over breakpoint configurations, or construct candidates explicitly and use local search.
