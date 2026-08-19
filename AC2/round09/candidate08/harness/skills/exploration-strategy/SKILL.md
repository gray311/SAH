---
name: exploration-strategy
description: Exploration over exploitation - Try completely new function families rather than incremental step-function edits.
---

# Exploration Strategy for C2 Optimization
## Why Diversity Matters The seed uses sophisticated step functions achieving 0.89628. To beat this, we need **orthogonal search directions** - fundamentally different mathematical constructions.
## Experiment Families
### 1. Spline Functions - **Idea**: Replace discontinuous steps with smooth cubic splines - **Implementation**: Use scipy.interpolate.CubicSpline - **Advantage**: Smoother convolution, less oscillation - **Try**: 8-12 control points, optimize positions and heights
### 2. Fourier-Based Construction - **Idea**: Optimize in Fourier space, transform back - **Implementation**: Modify FFT convolution with coefficient optimization - **Advantage**: Exploits spectral properties of optimal functions - **Try**: 10-20 Fourier modes with positivity constraints
### 3. Gaussian Mixtures - **Idea**: f(x) = Σ w_i * N(x; μ_i, σ_i) - **Implementation**: Parametric mixture model - **Advantage**: Smooth, analytically tractable, positive by construction - **Try**: 5-12 components, optimize all parameters
### 4. Piecewise Polynomials - **Idea**: Quadratic/cubic segments instead of constants - **Implementation**: Define breakpoints, fit polynomials per segment - **Advantage**: More flexible than steps, smoother than raw polynomials - **Try**: 2nd or 3rd degree, 6-10 pieces
## Execution Protocol 1. Generate a complete function family (use generate_function_family tool) 2. Implement the full EVOLVE-BLOCK from scratch 3. Evaluate (costs ~1 eval) 4. If c2 > 0.89628, try to refine (add 2-3 more parameters) 5. If no improvement in 2 tries, abandon and try new family
## Avoid These Pitfalls - Don't tweak step heights by 0.01 - trivial edits won't beat 0.89628 - Don't run the same family twice without modification - Don't exceed 30% time per experiment (abort and retry)
