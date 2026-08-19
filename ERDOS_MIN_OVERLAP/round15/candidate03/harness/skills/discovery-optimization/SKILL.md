---
name: discovery-optimization
description: "Use hard step-function initializations and coarse-to-fine search to escape local minima."
---

# Hard Step Function Strategy for Erdos Optimizer

## Problem
The seed uses sigmoid-smoothed latents, which all produce similar Gaussian-like shapes. This is a local optimum.

## Solution
Create HARD PIECEWISE CONSTANT initializations:

### Pattern 1: 3-Block Function
h(x) = a on [0,x1), b on [x1,x2), c on [x2,2]
Choose breakpoints like [0.5, 1.0, 1.5] or [0.33, 1.0, 1.67]

### Pattern 2: Support Split
h(x) = 0 on [0,a), 1 on [a,2]

### Pattern 3: Multi-Block
4-5 blocks with different heights and widths

### Implementation
Replace the _get_best_initialization to directly return step-function arrays (no sigmoid):
  - Create arrays of 0s and 1s (or 0.5s) at specific breakpoints
  - Ensure integral = 1 by adjusting widths

### Screening
Use probe_solution to check c5_bound quickly. Only evaluate if c5_bound < 0.375.

### Coarse-to-Fine
Try num_intervals=100 first, then increase to 800 for refinement.

## Why This Works
Step functions have sharp transitions that smooth latents cannot capture. The FFT evaluator rewards specific support patterns, not smooth curves.
