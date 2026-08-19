---
name: c2-function-families
description: Mathematical playbook for C2 optimization. Focus on testing completely different function families rather than incremental edits. Each evaluation should explore a new construction approach.
---

# C2 Function Family Exploration

## Objective
Achieve combined_score > 1.0 (C2 > 0.8962799441554086)

## Core Principle
With ~20 evaluations, test fundamentally DIFFERENT function constructions. Each eval
should be a different mathematical family, not parameter tuning of the same function.

## Function Families to Systematically Test

### 1. Multi-modal Piecewise Linear
- Multiple linear segments creating multiple peaks
- Design carefully to concentrate autocorrelation energy
- Example: peaks at x = +/-0.5, +/-1.0 with linear interpolation

### 2. Gaussian Mixtures
- Sum of Gaussians: f(x) = sum w_i exp(-(x-mu_i)^2/(2*sigma_i^2))
- Can create smooth multi-peaked functions
- Tune weights, centers, and widths

### 3. Piecewise Cubic / B-spline-like
- Smooth cubic segments with controlled continuity
- More flexible than linear pieces
- Example: sin^2-based constructions

### 4. Exponential Mixture
- Sum of decaying exponentials: f(x) = sum w_i exp(-lambda_i|x - mu_i|)
- Good for asymmetric decay patterns

### 5. Symmetric Double Peaks
- Exploit even symmetry: f(x) = f(-x)
- Two symmetric peaks, often efficient
- Can reduce optimization complexity

### 6. Multi-level Step Functions
- Discrete levels with multiple plateaus
- Refined version of the current champion (step function)
- Use more levels, asymmetric heights

### 7. Smoothed Transitions
- tanh-based smoothed steps
- Combines step-function efficiency with smoothness

### 8. Multi-scale Combinations
- Sum of functions at different scales
- Broad background + narrow peaks
- Example: wide Gaussian + narrow Gaussians

## Testing Protocol

1. Iteration 1-3: Test 3 completely different families
2. Iteration 4-8: Refine top 2 families with parameter variations
3. Iteration 9-15: Test 5 more diverse families
4. Iteration 16-20: Deep refinement of best candidates

## Success Patterns

- Step functions with multiple levels worked well (current baseline: 0.89628)
- Adding symmetry often helps
- Multi-peaked functions concentrate energy effectively
- Smooth transitions between peaks may help

## Failure Patterns

- Simple Gaussian alone: ~0.886 (underperforms)
- Single peak: harder to beat step functions
- Too many parameters: optimization struggles
- Asymmetric functions: harder to optimize

## Key Insight

The step function works because it concentrates probability mass efficiently.
Generalize this: any construction that concentrates ||f**f||_2^2 while keeping
||f**f||_1 and ||f**f||_inf controlled will beat the baseline.
