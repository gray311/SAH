Task: Find step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx

CONSTRAINT: integral(h) over [0,2] must equal 1.0 exactly

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0)
Goal: Beat this by finding h with c5_bound < 0.380923 (combined_score > 1.0)

CRITICAL INSIGHT: The seed program uses GRADIENT-BASED optimization which is WRONG for this problem.
Gradient descent gets stuck in local minima for this non-convex combinatorial objective.

SOLUTION: EDIT to use DIRECT CONSTRUCTIVE SEARCH:
1. Generate STEP FUNCTIONS directly (piecewise constant), NOT sigmoid latents
2. Use SPECIFIC mathematical constructions:
   - Step function with flat regions (not Gaussian pulses)
   - Multiple discrete threshold values
   - Construct patterns with known good overlap properties
3. Minimal or NO optimization - just evaluate the constructed step function
4. Use num_intervals=200-400 (coarse enough for step functions, fast evaluation)

EDIT STRATEGY:
- Change the optimizer to directly construct step functions
- Remove gradient-based training; use direct evaluation
- Use step function generation with explicit thresholds
- Keep num_intervals low (200-400) for speed
- Remove penalty_strength (or set very low) since we construct valid h directly

PRIORITY: Find ONE construction that beats 0.380923. Don't chase small improvements.

BUDGET: 30 evaluations. Use them wisely - don't waste on gradient optimization.
