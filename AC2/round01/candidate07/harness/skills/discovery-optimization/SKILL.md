---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize C\u2082 for the second autocorrelation inequality. Under fixed evaluation budget (20 full evaluations), use probe_solution for cheap ranking of variants. Explore different function representations (piecewise-constant, piecewise-linear, splines, Fourier-based, Gaussian mixtures, exponential combinations). Try multi-scale optimization and multi-start strategies. Combine targeted editing with probe-based exploration to find novel high-scoring functions."
---

# C₂ Optimization Strategy

## Objective
Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}), where f is a non-negative function. Theoretical upper bound: 1.0. Current best: 0.8963 (step functions).

## Available Resources
- Full evaluations: ~20 budget (use sparingly)
- Probes: Unlimited (~10s each, subsampled data, approximate scores for ranking)
- Function representation: Edit the EVOLVE-BLOCK to change the optimization approach

## Strategy Template

### Phase 1: Coarse Exploration
1. Use `probe_solution` to rapidly test different function representations:
   - Piecewise-constant (like step functions)
   - Piecewise-linear (current approach, but try different intervals)
   - Gaussian mixture models
   - Exponential decay combinations
   - B-spline basis functions
   - Fourier-series-based functions

2. For each representation, try:
   - Different number of parameters/intervals (10, 20, 50, 100, 200)
   - Different initialization strategies (random, structured, from priors)
   - Different optimizers (Adam, gradient descent with momentum, L-BFGS)

3. Use probe scores to rank candidates, then confirm top 3-5 with `evaluate_solution`

### Phase 2: Refinement
1. Take the best-performing representation from Phase 1
2. Increase optimization budget: more intervals, more steps, better learning rate schedule
3. Try multi-scale approach: coarse grid optimization → fine grid refinement
4. Use ensembles: average multiple locally optimal functions

### Phase 3: Targeted Search
1. Analyze why top-scoring functions work (symmetries, support structure)
2. Design new functions inspired by successful patterns
3. Fine-tune with local optimization

## Function Representation Priors
- **Step functions**: Worked well historically (0.8963). Easy to parameterize.
- **Piecewise-linear**: Current seed approach. Can improve with more intervals and better initialization.
- **Gaussian mixtures**: Smooth, convex-like behavior. Parameterize means, variances, weights.
- **Exponential combinations**: decay rates + shape parameters. Often smooth.
- **B-splines**: Local support, flexible shape control. Parameterize knots and coefficients.
- **Fourier-based**: Parameterize Fourier coefficients with constraints.

## Key Technical Considerations
- Ensure f(x) ≥ 0 everywhere (use softplus, relu, or exponential transformations)
- Use FFT for efficient convolution (O(n log n) vs O(n²))
- Adaptive discretization: coarse → fine
- Multiple random seeds for stochastic optimization
- Document versions for reproducibility

## Tool Usage
- `probe_solution`: Test 5-10 variants quickly before full eval
- `evaluate_solution`: Confirm top 3-5 candidates; these consume your 20 eval budget
- `edit_solution`: Make targeted changes. Prefer SEARCH/REPLACE diffs for small edits. Full rewrites for structural changes.

## Recovery Strategy
- If `validity = 0`, fix the error immediately
- If score regresses, try a different function class (not just parameter tuning)
- When stuck, reset with new representation + multi-start

## Budget Discipline
- ~15-18 probes per variant exploration
- 3-5 full evaluations for promising candidates
- Never repeat the same code
- When evals run low, consolidate on the best idea
