---
name: discovery-optimization
description: "Systematic exploration of function spaces beyond step functions. Uses function_scorer to identify promising patterns, then code_scaffold to inject entirely new function representations (cosine, spline, Gaussian mixtures) for evaluation."
---

# Function Space Exploration Protocol

## Phase 1: Identify Promising Step Patterns

1. Call function_scorer ONCE to analyze the current 13 step patterns

2. Note which patterns have highest C2 - these may serve as baselines

3. Identify mathematical properties: symmetry, peak spacing, height ratios


## Phase 2: Inject New Function Representations

Use code_scaffold to ADD new functions. Start with ONE class:

Cosine-Based Function (smooth, periodic-like):
x = jnp.linspace(0, 2*jnp.pi, n)
f = amp * jnp.cos(freq * x + phase)
f = jax.nn.relu(f)

Gaussian Mixture (smooth multi-peak):
x = jnp.linspace(0, 2.0, n)
f = jnp.zeros(n)
for i in range(num_components):
    center = (i + 1) / (num_components + 1)
    amp = 0.3 + i * 0.25 * scale_factor
    sigma = 0.15 + i * 0.05 * scale_factor
    f = f + amp * jnp.exp(-((x - center) / sigma)**2)

Piecewise Linear Spline (controlled smoothness):
knots = jnp.linspace(0.0, 2.0, num_knots + 2)
values = jnp.zeros(num_knots + 1)
for i in range(num_knots):
    height = 0.5 + 0.1 * i
    values = values.at[i].set(height)

For each new function, replace the ENTIRE function creation code or add it as an alternative.

## Phase 3: Evaluate and Refine

1. Evaluate the NEW function representation

2. If it improves: refine parameters (amplitude, frequency, widths)

3. If it fails: try a different function class


## Key Principles

- FUNCTION CLASS > PARAMETER TWEAKING: A cosine function can outperform any step function
- ONE at a time: Implement, evaluate, learn, then try the next class
- Mathematical grounding: Understand WHY a class should work before implementing
