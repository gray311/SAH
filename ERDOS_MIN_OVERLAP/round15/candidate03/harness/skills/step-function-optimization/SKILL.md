---
name: step-function-optimization
description: Use hard piecewise constant initializations and coarse-to-fine search.
---

# Step Function Optimization for Erdos Problem

## Strategy
Replace sigmoid-smoothed latents with HARD step functions.

## Initializations

### 2-Block
h(x) = a on [0,x1), 0 on [x1,2]
Constraint: a*x1 = 1 => x1 = 1/a. Try a=0.6 (x1=1.67), a=0.8 (x1=1.25)

### 3-Block
h(x) = h1 on [0,x1), h2 on [x1,x2), 0 on [x2,2]
Constraint: h1*x1 + h2*(x2-x1) = 1
Try: h1=1, h2=0.5, x1=0.5, x2=1.0 then normalize

### 4-Block
h(x) = h1 on [0,x1), h2 on [x1,x2), h3 on [x2,x3), 0 on [x3,2]
More flexibility for low overlap.

## Editing the Seed

1. Replace _get_best_initialization to directly create step arrays
2. In _objective_fn, remove sigmoid: h = step_array
3. Set num_restarts=1 to focus on that one pattern
4. Increase learning rate to 0.01 or 0.02

## Screening
Use probe_solution to quickly check c5_bound. Only evaluate if c5_bound < 0.375.

## Coarse-to-Fine Option
Start with num_intervals=100, optimize, then increase to 800 for refinement.
