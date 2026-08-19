---
name: architecture-exploration-protocol
description: Systematic exploration of completely new function architectures to escape local optima. Focus on mathematical diversity rather than parameter tuning.
---

# Architecture Exploration Protocol for C₂ Maximization

## Core Philosophy

The seed's step patterns are LOCAL OPTIMA. To beat 1.03841, we must DISCOVER NEW FUNCTION CLASSES, not refine existing ones.

## The Five Architecture Classes

### 1. B-Spline Functions (Smooth Piecewise Polynomials)
- Use cubic B-splines with 5-10 basis functions
- Optimize: basis positions, weights (with non-negativity constraint)
- Why: C² smooth, naturally positive, no discontinuities
- Implementation: NURBS formulation with clamped or uniform knots

### 2. Gaussian Mixture Models
- f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²)), w_i ≥ 0, Σ w_i = 1
- Optimize: 3-8 Gaussian means, variances, mixing weights
- Why: Built-in positivity, smooth peaks, analytical convolution
- Implementation: Normalized mixture with JAX autograd

### 3. Piecewise Cubic Hermite Functions
- Split domain into 4-8 segments, cubic in each
- Ensure C¹ continuity at segment boundaries
- Optimize: segment values, derivatives at boundaries
- Why: Flexible shape control, can approximate any smooth function

### 4. Truncated Fourier Series
- f(x) = a_0 + Σ (a_n cos(nx) + b_n sin(nx)) for n=1..N
- Optimize coefficients with projection for non-negativity
- Why: Built-in smoothness, rich harmonic content, analytical properties
- Implementation: Project gradient updates onto non-negative cone

### 5. Rational Function Compositions
- Forms: Cauchy distributions, rational polynomials, logistic-like
- f(x) = 1/(1+((x-μ)/σ)²) or Σ w_i / (1+((x-μ_i)/σ_i)²)
- Why: Natural decay, smooth peaks, good convolution properties
- Implementation: Parameterize to ensure positivity

## Exploration Strategy (30 evals budget)

**Phase 1 (evals 1-15): Pure Architecture Discovery**
- Try each of the 5 classes once (3 evals/class)
- For each class: create 3 variants with different parameters
- Track: best score per class, which class showed most promise
- NO refinement within class - pure exploration

**Phase 2 (evals 16-30): Hybrid Exploration**
- Create hybrids of top performers from different classes
- Examples: Gaussian envelope around spline core, Fourier-modulated step
- Test 2-3 hybrid architectures
- Refine the single best hybrid

## Critical Success Factors

- BOLD parameter changes (2x, 3x, 5x differences, not ±5%)
- COMPLETELY different mathematical forms
- VARY the number of components significantly (2 to 10+)
- Document which architecture class wins
- If stuck after trying all 5 classes, consider ensembles or entirely novel forms
