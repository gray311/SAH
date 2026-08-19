You are optimizing for C5 bound. Goal: MAXIMIZE combined_score = 0.38092303510845016 / c5_bound.
Current best: 0.999641 (c5_bound ≈ 0.380975). Target: combined_score > 1.0 (c5_bound < 0.380923).

**CONSTRAINTS**: h:[0,2]→[0,1], integral(h)=1 exactly.

**WHY WE'RE STUCK**: The seed uses Adam optimization with 800 intervals. Gradient-based methods get trapped in local optima for this non-convex problem.

**YOUR TASK**: Rewrite the EVOLVE-BLOCK to try fundamentally different approaches:

1. **Discrete pattern search**: Instead of continuous optimization, try SPECIFIC step function patterns:
   - Single block: h=1 on [0,1], h=0 elsewhere (integral=1)
   - Two-block: h=a on [0,x], h=b on [y,2] with 2ax + (2-y)b = 1
   - Uniform + perturbation: h=0.5 + small structured perturbations

2. **Fewer intervals first**: Start with num_intervals=200 (coarse), optimize, then increase to 800

3. **Alternative optimization**: Try coordinate descent on piecewise constant h (fix all but one interval, optimize that one)

4. **Pattern-based initialization**: Use the _get_best_initialization method but with CONCRETE mathematical patterns, not random noise.

5. **Evaluate multiple variants per edit**: Make edits that create 2-4 distinct candidate solutions, then eval each.

**EDITING RULES**:
- When changing initialization: rewrite the entire _get_best_initialization method
- When changing optimization: modify _objective_fn and how trains run
- Always ensure h values are sigmoid-transformed or clamped to [0,1]
- Always enforce integral=1 via penalty (seed uses penalty_strength=1370)

**BUDGET**: ~30 evaluations. Each eval is precious. Spend on promising directions.

**AGENCY**: Complete rewrites are expected. Don't make small edits.
