---
name: discovery-optimization
description: "Find discrete step functions with sharp boundaries, not smooth sigmoid curves. Use probes to screen piecewise constant candidates."
---

# Discrete Step Function Strategy for Erdos Optimizer

## Why Smooth Functions Fail
The seed's 12 patterns all produce smooth sigmoid curves. The optimal Erdos solution likely requires TRUE STEP FUNCTIONS with sharp boundaries.

## Workflow

### Phase 1: Generate Discrete Step Functions
Call generate_discrete_steps to create piecewise constant functions:
- Rectangle pulses: sum of indicator functions on [a_i, b_i)
- Multi-interval constructions: disjoint intervals with different heights
- Symmetric vs asymmetric patterns

### Phase 2: Enforce Exact Constraint
For each step function:
1. Compute integral exactly: sum of (height * width) for each interval
2. If integral != 1, rescale or adjust interval widths
3. Only consider functions with integral = 1 (within numerical tolerance)

### Phase 3: Probe and Evaluate
- Use probe_solution on step functions with valid integral
- Target: c5_bound < 0.37 (below current best 0.3809)
- Full evaluation only on best 2-3 step function candidates

### Phase 4: If No Success, Direct Edit
Replace _get_best_initialization with a direct piecewise constant constructor:
```python
def _get_best_initialization(self, seed):
    # Directly return a piecewise constant latent (no sigmoid!)
    # Specify intervals and heights explicitly
```

## Critical: Avoid Sigmoid
The seed applies jax.nn.sigmoid(latent). For step functions, either:
- Skip sigmoid entirely and use step functions as latent
- Use sigmoid with very large magnitude to approximate step function behavior

## Expected Outcome
- True step functions can achieve lower C5 than smooth curves
- Piecewise constant functions match the "step function" problem statement
