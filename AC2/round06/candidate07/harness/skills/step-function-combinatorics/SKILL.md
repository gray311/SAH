---
name: step-function-combinatorics
description: Method playbook for C2 optimization using step function combinatorics. Systematic exploration of symmetric/asymmetric configurations. Probe before eval discipline.
---

# Step Function Combinatorics for C2 Maximization

## Objective
Maximize C2 > 0.8963. Record: 0.8963. Seed: 1.02665. Target: > 1.02872.

## Core Principle: TRUE STEP FUNCTIONS
The seed's piecewise-linear optimization is weak. Use jnp.piecewise to create piecewise-CONSTANT functions (flat regions, not ramps).

## Symmetric Configurations

### 2-Step (Single Peak)
f(x) = h for |x| < w, 0 otherwise
Code: f = jnp.piecewise(x, [x < -w, abs(x) < w, x > w], [0.0, h, 0.0])

### 3-Step (Bimodal)
f(x) = h1 for |x| < w1, h2 for w1 < |x| < w2, h1 for |x| > w2
Code: f = jnp.piecewise(x, [x < -w2, abs(x) < w1, w1 <= abs(x) <= w2, abs(x) > w2], [0.0, h1, h2, 0.0])

### 4-Step (Four peaks)
Two on each side of 0: left_outer < left_inner < center < right_inner < right_outer

## Asymmetric Configurations

### Shifted Peak
f(x) = h if c - w < x < c + w, else 0
Code: f = jnp.piecewise(x, [x < c - w, abs(x - c) < w, x > c + w], [0.0, h, 0.0])

### Multiple Clusters
Three separate peaks at positions p1, p2, p3

## Implementation Pattern

1. Use step_function_builder tool for code generation
2. Edit seed to replace _create_step_initializer with jnp.piecewise
3. Remove jax.nn.relu - it destroys the step structure
4. Probe variants, evaluate top 2-3

## Probe-Before-Eval Discipline
- Generate 5-8 step configurations
- Probe each (call probe_solution)
- Rank by probe score
- Evaluate ONLY top 2-3
- MAX 4 full evaluations total

## Fallback Strategies
If step functions stall:
1. Polynomial decay: f(x) = exp(-alpha * |x|^beta)
2. Gaussian mixture: sum of Gaussians
3. Seed's multi-start with different initializations
