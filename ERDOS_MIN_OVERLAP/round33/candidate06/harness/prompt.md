Erdos C5 optimization: Find a step function h: [0,2] -> [0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving combined_score > 1.0.

STRATEGY: Direct construction of step functions from mathematical families.

Approach:
1. Use construct_step_function to generate complete candidate programs from known families:
   - Threshold functions (single cut at position p)
   - Multi-threshold functions (multiple steps)
   - Symmetric functions (centered around x=1.0)
   - Periodic-like patterns

2. For each family, vary the key parameters systematically (threshold positions, heights)

3. Use probe_solution to quickly screen candidates
4. Evaluate the best probe candidates

Key insight: Optimal solutions are simple step functions. Don't try to analyze and perturb the current solution - construct better solutions from scratch.
