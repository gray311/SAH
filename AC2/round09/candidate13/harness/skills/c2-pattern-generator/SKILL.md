---
name: c2-pattern-generator
description: Generate diverse piecewise-constant functions for C2 maximization. Focus on pattern classes - symmetric pyramids, asymmetric multi-step, bimodal, narrow peaks, wide plateaus.
---

# C2 Pattern Generation Guide

## Function Classes for C2 Maximization

### 1. Symmetric Pyramid
Pattern: low-high-med-high-low
Heights: [0.6, 1.4, 2.1, 1.4, 0.6]
Widths: 20%, 40%, 20%
Rationale: Symmetry helps balance the convolution properties

### 2. Asymmetric Multi-Step
Pattern: gradual rise with plateau
Heights: [0.8, 1.2, 1.8, 1.5, 1.0]
Widths: 15%, 25%, 25%, 20%, 15%
Rationale: Breaking symmetry to explore local optima

### 3. Bimodal Function
Pattern: two peaks with central valley
Heights: [0.9, 0.3, 1.9, 0.3, 1.1]
Widths: 20%, 15%, 30%, 15%, 20%
Rationale: Separated energy concentrations

### 4. Narrow High Peak
Pattern: concentrated energy
Heights: [0.5, 0.5, 2.8, 0.5, 0.5]
Widths: 20%, 20%, 30%, 20%, 10%
Rationale: Testing boundary cases with high peak

### 5. Wide Plateau with Bump
Pattern: uniform with single enhancement
Heights: [1.2, 1.2, 1.2, 1.6, 1.2]
Widths: 30%, 10%, 30%, 20%, 10%
Rationale: Baseline with localized improvement

## Parameter Search Strategy

For each class, search:
- Height: ±0.1 from base (5 values)
- Width: ±5% of interval (3 values)
- Position: ±10% of interval (2 values)

Total variants per class: 5×3×2 = 30 (exhaustive for small grids)

## Local Optimization

After identifying promising patterns:
1. Use learning rate 0.15-0.25
2. Run 5000-7000 iterations
3. Reinitialize every 500 iterations (perturb 20% of heights by ±0.05)
4. Track best_c2 and stagnation_window=100

## Critical Success Factors

- Ensure all heights are positive (use relu or explicit checks)
- Normalize total integral if needed
- Use FFT-based convolution for speed
- Compute L2 norm with trapezoidal rule for accuracy
