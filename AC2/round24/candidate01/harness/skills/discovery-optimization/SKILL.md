---
name: discovery-optimization
description: "Architectural exploration for C2 maximization. Test multiple function families (step, Gaussian, spline, polynomial), refine best, use probes for rapid screening."
---

# C2 Maximizer: Architectural Exploration Protocol

## Core Principle
The current best (step functions) achieves ~0.934. New architectures may exceed 0.95. Test multiple families with probes, then refine the winner.

## Function Families to Test

1. **Step Functions** (seed baseline): Piecewise constants, already achieves 0.934

2. **Smoothed Step Functions**: Convolve step function with Gaussian kernel (sigma = 0.05-0.2)
   - Benefits: Smooth edges, avoids numerical instability

3. **Gaussian Mixtures**: f(x) = sum w_i * exp(-(x-mu_i)^2/(2*sigma_i^2))
   - Constraints: w_i >= 0, sum w_i = 1, tune mu_i, sigma_i, w_i

4. **B-splines**: Piecewise polynomial with optimized knot positions and weights

5. **Polynomial Bases**: f(x) = sum a_k * x^k for x in [a,b], zero elsewhere

## Phase 1: Architecture Screening (iterations 1-10)

Step 1: Rapid Family Comparison
- Call compare_architectures (generates 1 variant per family, uses 5 probes)
- Identify top 2 families by probe score

Step 2: Deep Exploration
- Generate 2-3 variants in each top family
- Probe all variants (total: 5 + 6-9 probes = 11-14 probes)
- Evaluate top 1-2

Step 3: Refine Winner
- Apply smart perturbations to best variant
- Iterate until stuck or budget exhausted

## Phase 2: Deep Refinement (iterations 11-25)

Step 1: Gradient-Based Search
- Use JAX autodiff to compute gradients w.r.t. all parameters
- Generate 3 variants: (a) ascent, (b) descent, (c) orthogonal direction

Step 2: Probe and Evaluate
- Probe all 3, evaluate best
- If gradient norm < 0.001 or no improvement in 3 iterations: reinitialize

Step 3: Reinitialization
- Keep top 30% of parameters, randomize remaining

## Phase 3: Aggressive Search (iterations 26-30)

Step 1: New Families
- Try 2-3 new architectures: (a) rational functions, (b) trigonometric polynomials, (c) mixture of Gaussians and polynomials

Step 2: Final Probe-Eval Loop
- Probe all, evaluate best, submit if c2 > 0.8962799441554086

## Key Rules

- ALWAYS call compare_architectures at iteration 1 and if stuck
- Use probes to explore 8-10 variants before any full eval
- Don't overfit to step functions - test smooth alternatives
- JAX autodiff works on any differentiable function
