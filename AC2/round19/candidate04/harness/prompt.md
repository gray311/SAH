You are optimizing the C2 constant for the second autocorrelation inequality.
Target: exceed 0.8962799441554086 (current best from step functions).

CURRENT STATUS: The seed program uses 11 step-function patterns but ALL achieve the same score (1.042 combined).
CRITICAL: Small mutations within step functions CANNOT escape this local optimum.

STRATEGY - DIVERSE FUNCTION GENERATION:

PHASE 1 (iterations 1-15): BROKEN SYMMETRY EXPERIMENTS
1. Generate a NEW function type entirely (NOT step function mutations)
   Options: Gaussian mixture, B-spline, piecewise-linear, oscillatory decay
2. Edit the EVOLVE-BLOCK to implement this new function
3. Call probe_solution on your edit
4. If probe score indicates promise, call evaluate_solution
5. Track which function families work

PHASE 2 (iterations 16-30): HYPOTHESIS REFINEMENT
1. If Phase 1 found improvement: refine that function family with targeted changes
2. If no improvement in Phase 1: try a DIFFERENT function family
3. Always call probe_solution before evaluate_solution

FUNCTION FAMILY TEMPLATES (choose ONE and implement):

FAMILY A - Gaussian Mixture:
  f(x) = sum_i w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
  - n_gaussians in [2,4], mu in [-2,2], sigma in [0.3,1.5], weights sum to ~1
  
FAMILY B - Oscillatory with Decay:
  f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*|x|)
  - alpha in [0.2, 0.6], beta in [3, 8], gamma in [0.5, 1.2]

FAMILY C - Piecewise-Linear with Symmetry:
  - 5-7 vertices symmetric around x=0
  - Heights: [h1, h2, h3, h2, h1] with h1 in [0.5, 1.0], h2 in [1.2, 2.5], h3 in [1.8, 3.0]

FAMILY D - Multi-Step Asymmetric:
  - 3-4 step levels with varying heights
  - Heights: [0.6, 1.5, 2.3] at positions [0.1, 0.35, 0.6, 0.85]

RULES:
- NEVER stay in step functions - they're proven to be stuck
- ALWAYS probe before full evaluation
- Use edit_solution with precise parameter changes
- Document in scratch what you tried and why
