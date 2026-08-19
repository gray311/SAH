---
name: discovery-optimization
description: "Find simple piecewise constant step functions to achieve low C5 bounds."
---

# Simple Step Function Strategy for Erdos Optimizer

## Key Insight
The optimal C5 minimizer is likely a SIMPLE step function with 2-4 segments, not a complex 800-interval function.

## Strategy

### Phase 1: Try Simple 2-3 Segment Functions (DO THIS FIRST)

Use create_piecewise_init to generate candidates with 2-4 segments. For each candidate:
1. EDIT the seed to use num_intervals=10-20
2. EDIT _get_best_initialization to return ONLY that piecewise function
3. Call probe_solution to check c5_bound < 0.37
4. Call evaluate_solution if probe passes

### Phase 2: If No Simple Solution, Try Seed Optimizer

If all simple functions fail, try the seed optimizer with diverse init using num_intervals=50-100.

## Why Simple Functions Work
- Fewer segments = less overlap between h(x) and h(x+k)
- Disjoint support minimizes the integral
- The FFT-based evaluator rewards sparsity and separation
