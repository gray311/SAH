---
name: discovery-optimization
description: "Architecture-first C\u2082 maximization. Generate and evaluate completely different function classes (splines, Gaussian mixtures, piecewise polynomials, Fourier series, rational functions) before refining existing patterns. Explores novel mathematical forms that can escape the local optimum of step functions."
---

# Architecture-First C₂ Maximization Protocol

## Core Principle

The seed's step patterns are locally optimal. Small mutations won't help. We must DISCOVER NEW FUNCTION CLASSES.

## Phase 1: Architecture Exploration (evals 1-15)

**Architecture Class A: Smooth B-Spline Functions**
- Use cubic B-splines with 5-10 basis functions
- Optimize: basis positions, weights (ensure non-negative)
- Advantage: C² smooth, no discontinuities

**Architecture Class B: Gaussian Mixture Models**
- f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²)) with w_i ≥ 0, Σ w_i = 1
- Optimize: 3-8 Gaussians, positions, widths
- Advantage: Naturally positive, smooth transitions

**Architecture Class C: Piecewise Cubic Hermite**
- Split domain into 4-8 segments
- Each segment: cubic polynomial with controlled derivatives
- Ensure C¹ continuity at boundaries

**Architecture Class D: Truncated Fourier Series**
- f(x) = a_0 + Σ (a_n cos(nx) + b_n sin(nx)) for n=1..N
- Optimize coefficients with non-negativity constraint
- Advantage: Built-in smoothness, analytical properties

**Architecture Class E: Rational Function Compositions**
- f(x) = 1 / (1 + (x-μ)²/σ²) or similar rational forms
- Can combine multiple rational functions
- Advantage: Decay properties, smooth peaks

## Phase 2: Cross-Architecture Combinations (evals 16-30)

- Hybrid: Step function envelope around smooth core
- Hybrid: Gaussian mixture with piecewise modulation
- Ensemble averages of top functions from different classes

## Execution Strategy

1. Pick an unexplored architecture class
2. Generate 3 distinct implementations with different parameters
3. Evaluate all 3 (use 3 evals per architecture)
4. Select best, optionally refine with 1-2 small tweaks
5. Move to next class after exhausting current one
6. In final phase, combine top performers from different classes

## Success Criteria

- Beat 1.03841 by at least 0.005 (reach 1.043+)
- Achieve this with a completely different function class than step functions
- Document which architecture class produced the best result
