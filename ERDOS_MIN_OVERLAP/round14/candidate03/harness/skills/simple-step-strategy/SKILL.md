---
name: simple-step-strategy
description: Find low-C5 solutions using simple 2-4 segment step functions before complex optimizations.
---

# Simple Step Function Strategy

## The Key Insight

The optimal C5 minimizer is likely a VERY SIMPLE step function with 2-4 segments, not a complex 800-interval function learned by Adam optimization.

## Action Plan

1. IMMEDIATELY use create_piecewise_init to generate 2-4 segment functions

2. For EACH candidate from create_piecewise_init:
   - EDIT the seed to use ONLY that candidate (replace _get_best_initialization)
   - Set num_intervals=10-20 (simple function needs simple discretization)
   - Set num_steps=2000-5000 (no need for long optimization)
   - Set num_restarts=1
   
   3. Call probe_solution to check:
      - c5_bound < 0.37
      - integral(h) approx 1 (should be satisfied by construction)
   
   4. Call evaluate_solution on the best 1-2 probe candidates

5. If no success after trying all simple candidates, THEN try the seed optimizer with diverse init

## Why Simple Functions Work

- Fewer segments = less overlap between h(x) and h(x+k)
- Disjoint support (h and 1-h don't overlap much) minimizes the integral
- The FFT-based evaluator rewards sparsity and separation
