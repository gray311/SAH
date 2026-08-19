---
name: erdos-step-function-strategy
description: Method for optimizing step functions in Erdos minimum overlap problem. Use coarse-to-fine discretization, explicit pattern construction, and structural simplification.
---

# Step Function Optimization for Erdos C5 Problem

## Why the Seed Fails
The seed uses 8000 intervals with sigmoid parameterization. For a step function problem:
- Over-parameterization leads to local optima
- Gradient descent struggles with non-smooth objectives
- Sigmoid produces smooth transitions, not sharp steps

## Strategy 1: Coarse-to-Fine
Start with 16-32 intervals. Optimize to convergence. Then:
1. Save the optimized boundary points
2. Add new boundaries between existing intervals
3. Optimize the new function on refined grid
4. Repeat until desired resolution

## Strategy 2: Explicit Patterns
Try these initializations:
Pattern A: h(x) = 0.5 for x < 1, 0.0 for x >= 1
Pattern B: h(x) = 1.0 for x < c, 0.0 for x >= c (c in [0,2])
Pattern C: Three-step: h(x) = a for x < c1, b for c1 <= x < c2, 0.0 otherwise
Pattern D: Symmetric: h(x) = a for x < c, b for c <= x < 2-c, a for 2-c <= x < 2
Then optimize parameters (a, b, c1, c2) via gradient descent or grid search.

## Strategy 3: Quantization
Assume h takes values from {0.1, 0.3, 0.5, 0.7, 0.9}.
For each interval, assign one of these values.
This is a discrete optimization over assignments + continuous optimization over boundaries.

## Strategy 4: Boundary-First Optimization
1. Fix interval values (e.g., alternating high/low)
2. Optimize only boundary positions
3. Reassign interval values based on optimal boundaries
4. Repeat 2-3

## Implementation Template
class CoarseToFineOptimizer:
    def __init__(self):
        self.start_intervals = 32
        self.refine_factor = 2
        self.max_refines = 4
        
    def _optimize_level(self, num_intervals, latent_dim=None):
        # Implement gradient-based optimization
        # Return optimized h array
        pass
        
    def _refine_boundaries(self, h_coarse):
        # Extract boundaries from coarse solution
        # Add intermediate boundaries
        # Return new function
        pass
        
    def optimize(self):
        h = self._optimize_level(self.start_intervals)
        for i in range(self.max_refines):
            h = self._refine_boundaries(h)
            h = self._optimize_level(len(h), latent_dim=len(h))
        return h
