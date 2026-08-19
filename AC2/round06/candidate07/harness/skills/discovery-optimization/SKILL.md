---
name: discovery-optimization
description: "Optimize C2 using step functions. Generate step configurations via step_function_builder, implement true piecewise-constant functions, probe before eval. Avoid gradient-based optimization."
---

# C2 Maximization: Step Function Strategy

## Objective
Maximize C2 = ||f * f||_2^2 / ((integral(f)^2) ||f * f||_infty). Record: 0.8963 (step functions). Seed baseline: 1.02665. Target: > 1.02872.

## Why Step Functions Win
Step functions (piecewise-constant) achieve the best known lower bounds. The seed's piecewise-linear approach with gradient descent is suboptimal.

## Strategy

### Phase 1: Symmetric Step Functions
Use jnp.piecewise to create functions like:
- f(x) = h1 for |x| < w1, h2 for w1 < |x| < w2, 0 otherwise
- Try heights: [1.0, 1.5], [1.2, 1.0, 1.3], [0.8, 1.0, 1.2]

### Phase 2: Asymmetric Step Functions
Create shifted peaks:
- Single peak at x = c: f(x) = h if |x - c| < w, else 0
- Two peaks at +c and -c: bimodal

### Phase 3: Multi-step Functions
3-5 steps with varying heights and widths:
- Left wing < center > right wing
- Multiple clusters

### Phase 4: Polynomial Decay (fallback)
f(x) = exp(-alpha * |x|^beta). Optimize alpha, beta via grid search.

## Execution Protocol

1. Call step_function_builder - get concrete intervals and heights
2. Edit the seed: Replace _create_step_initializer with jnp.piecewise that creates TRUE step functions (constant over intervals)
3. Probe: Call probe_solution on the edited code
4. Repeat: 5-8 variants, building a ranked list
5. Evaluate: Top 2-3 only with evaluate_solution
6. Fallback: If stuck, use polynomial decay

## Critical Rules
- MAX 4 full evaluations
- ALWAYS probe 5+ variants before any eval
- Use step_function_builder for structured exploration
- True step functions = constant over intervals, NOT linear ramps
- If stuck: switch to polynomial decay or Gaussian mixtures
