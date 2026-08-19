---
name: discovery-optimization
description: "C2 maximization via improved discretization and diverse function representations. Use analyze_discretization_quality to guide resolution choices, not just step-verification."
---

# C2 Maximization: Beyond Step Functions

## Critical Realizations

The seed program already creates valid step functions. The issue is NOT verification - it's NUMERICAL OPTIMIZATION.

## Key Strategies

### 1. Discretization Resolution

- SEED uses 400 intervals: moderate accuracy
- Try 800-1600 intervals: better accuracy, slower
- Use analyze_discretization_quality to decide optimal resolution

### 2. Function Representation Diversity

Don't just tweak step patterns. Explore:
- Gaussian mixtures
- Spline-based functions
- Fourier coefficient optimization
- Piecewise polynomial (not linear!)

### 3. Optimization Techniques

- **Multi-scale**: Optimize on coarse grid, refine on fine grid
- **Symmetry**: Use even functions f(x) = f(-x) to reduce parameters
- **Normalization**: Scale f so ∫f = 1 for fair comparison

## Workflow

1. Call analyze_discretization_quality FIRST
2. Based on feedback, edit discretization or function representation
3. Call analyze_discretization_quality to verify changes
4. Probe 3-5 variants
5. Evaluate best 1-2

## Common Pitfalls

- Wasting evaluations on same discretization
- Not trying different function families
- Ignoring numerical stability (padding, normalization)
- Over-optimizing coarse discretization (local minima)
