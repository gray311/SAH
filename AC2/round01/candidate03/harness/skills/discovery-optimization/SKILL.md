---
name: discovery-optimization
description: "Math discovery harness for C\u2082 constant optimization. Uses constructive search strategies (piecewise, spline-based functions) + refinement, not blind gradient ascent. Targets beating the step-function record of 0.8962799441554086."
---

# C₂ Constant Discovery: Constructive Search Strategy

## Objective
Beat C₂ = 0.8962799441554086 (step-function record) by discovering novel function classes.

## Why Current Approaches Fail
- Random initialization + Adam gradient ascent gets stuck in local optima
- The mathematical optimum is not a "smooth" point in parameter space
- Need CONSTRUCTIVE strategies: define function form, optimize parameters

## Phase 1: Coarse Construction
- Use 10-20 intervals initially
- Try SPECIFIC function classes:
  * Piecewise linear (linear segments between knots)
  * Symmetric piecewise (even functions)
  * Mixture models (weighted sums of Gaussians, exponentials)
- Manual initialization: start with known-good shapes (triangles, bumps)

## Phase 2: Refinement
- If coarse version achieves > 0.998 combined, increase to 50-100 intervals
- Fine-tune with Adam but try DIFFERENT starting shapes
- Consider: sharper transitions, multiple peaks

## Phase 3: Diverse Exploration
- If no improvement after 3-4 evals: try COMPLETELY different construction
- Vary function class, not just hyperparameters
- Examples to try:
  * Triangle pulse
  * Double-humped functions
  * Piecewise exponential decay
  * Spline-based constructions

## Key Constraints
- f(x) ≥ 0 everywhere (use relu or exp in code)
- Use jax for autograd; JIT the objective
- Respect budget: each evaluate_solution costs 1 of 20

## When Stuck
- Score < 0.995 after 2 evals: change function class
- Score < 0.998 after 4 evals: try symmetric construction
- < 0.99 after all evals: perhaps the discrete method has limits; still report best found

## Template Pieces
To construct a piecewise-linear function:
- Define knots: x_i = i / (num_intervals + 1)
- Define heights: h_i (positive, optimized)
- Interpolate linearly between (x_i, h_i)
- Use jnp.piecewise or manual construction

To construct a mixture:
- f(x) = sum_i w_i * exp(-((x - mu_i)/sigma_i)^2 / 2)
- Optimize weights, centers, widths with positivity constraints
- Use jax.nn.softplus for weights, exp for activation
