---
name: c2-function-exploration
description: A method playbook for discovering high-C₂ functions. Explores diverse function representations (step functions, piecewise-linear, Gaussian mixtures, B-splines, Fourier-based) using probe-based ranking before full evaluation. Focuses on structural innovation over parameter tuning.
---

# C₂ Function Exploration Playbook

## Overview
This playbook guides discovery of novel functions achieving high C₂ values for the second
autocorrelation inequality. Key insight: the function *representation* matters more than
hyperparameter tuning alone.

## Phase 1: Representation Exploration (18 probes)

Test these function classes, ranking by probe score:

### A. Piecewise-Constant (Step Functions)
- **Why**: Current record-holder (0.8963). Simple, interpretable.
- **Parameterize**: Array of N bin heights, all ≥ 0.
- **Probe budget**: 5-8 probes with N=10, 20, 50, 100
- **Variations**: Symmetric versions, asymmetric, support on different intervals

### B. Piecewise-Linear (Current Seed Approach)
- **Why**: Smooth transitions, continuous derivatives.
- **Parameterize**: N+1 node values (trapezoidal interpolation).
- **Probe budget**: 5-8 probes with N=10, 20, 50, 100, 200
- **Variations**: Symmetric triangular peaks, multi-modal, varying support width

### C. Gaussian Mixture Models
- **Why**: Smooth, localized peaks. Often optimal for integral-based problems.
- **Parameterize**: means (K), variances (σ²), weights (w), ensure non-negativity.
- **Probe budget**: 5-8 probes with K=2, 3, 5, 10
- **Variations**: Equal variance, adaptive variance, constrained support

### D. Exponential Combinations
- **Why**: Natural decay, positive everywhere.
- **Parameterize**: Sum of exponentials: Σ w_i * exp(-α_i * |x - μ_i|)
- **Probe budget**: 3-5 probes
- **Variations**: Single exponential, double exponential, mix with Gaussians

### E. B-Spline Basis Functions
- **Why**: Local support, C^k continuity control.
- **Parameterize**: Knot positions + spline coefficients.
- **Probe budget**: 3-5 probes
- **Variations**: Different knot placements, uniform vs adaptive knots

### F. Fourier-Space Optimization
- **Why**: Global parameterization, implicit smoothness.
- **Parameterize**: Fourier coefficients with inverse-FFT positivity check.
- **Probe budget**: 2-3 probes (complex setup)
- **Variations**: Low-frequency dominant, band-limited

## Phase 2: Multi-Scale Refinement (3-5 full evals)

Take top 3 representations from Phase 1:
1. Increase intervals/parameters by 2-3x
2. Use multi-start: 5 random initializations from each top representation
3. Refine hyperparameters (learning rate, steps) based on initial scores

## Phase 3: Ensemble & Hybridization
- Combine top performers: weighted averages, mixture models
- Analyze winning functions: extract structural properties (symmetry, support)
- Design new candidates inspired by successful patterns

## Best Practices
- **Use probes aggressively**: 15-18 probes per function class before eval
- **Diversify early**: Don't tunnel into one representation too soon
- **Record all probe scores**: Track which representation-family has best response
- **Reserve evals**: 3-5 full evaluations, each for the most promising variant
- **Validate function properties**: Ensure f(x) ≥ 0, ∫f > 0

## Common Pitfalls
- Over-tuning a single representation (likely local optimum)
- Insufficient probe exploration (missing the right representation family)
- Ignoring symmetry: Many optimal functions are even (f(-x) = f(x))
- Poor initialization: Start from informed priors, not random alone
- Getting stuck in smooth vs discontinuous debate: Test both families equally"
