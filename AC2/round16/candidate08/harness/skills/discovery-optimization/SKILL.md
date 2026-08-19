---
name: discovery-optimization
description: "Spectral variational search for C\u2082 maximization. Use mathematically orthogonal function spaces (Fourier eigenfunctions, Laguerre polynomials, variational trial functions) rather than mutating step patterns."
---

# Spectral Variational Protocol for C₂ Maximization

## Core Principle

Step functions are local optima. To break through, work in FUNCTION SPACES that are mathematically orthogonal to steps - not smooth steps, but fundamentally different representations.

## Function Space Hierarchy (try in order, exhaust each before moving on)

### Space 1: Fourier Eigenfunctions
f(x) = Σ_{k=1}^K c_k * φ_k(x) where φ_k are orthonormal basis functions (sine/cosine, Laguerre, Hermite)
- Start with K=3-5 terms
- Optimize coefficients c_k to maximize C₂
- Ensure f(x) ≥ 0 via softplus/post-processing

### Space 2: Variational Trial Functions
Use known optimality conditions from calculus of variations:
- Euler-Lagrange solutions for C₂ optimization
- Ansatz: f(x) = exp(-V(x)) where V(x) solves a variational problem
- Try: f(x) = (1 + α cos(βx))ⁿ * exp(-γ|x|) for n=2,3,...

### Space 3: Dense-Sparse Hybrids
Not step functions, but structured sparsity:
- f(x) = base_envelope(x) * (1 + sparse_features(x))
- base_envelope: smooth Gaussian or exponential decay
- sparse_features: localized bumps at optimized positions (not fixed step edges)

### Space 4: Hankel/Radial Functions
- f(x) = g(|x|) where g is optimized for radial symmetry
- Relate to spherical harmonics in higher dimensions

### Space 5: Hermite-Gaussian Functions
- Eigenfunctions of the Fourier transform
- Natural for convolution-optimized functions

## Exploration Protocol

1. Pick ONE function space from the hierarchy above
2. Generate 2-3 concrete implementations in that space
3. Evaluate each with evaluate_solution (NO PROBES - they are unreliable)
4. If no improvement after 3 evals: switch to a different space
5. Keep track of which space is most promising

## Key Mathematical Insights

- The C₂ constant is tied to spectral properties of f★f
- Fourier-domain optimization may reveal structure hidden in real space
- Variational methods can give analytic hints about optimal shapes
- Smooth functions with "bump" features (not steps) may achieve better L₂/∞ ratios
