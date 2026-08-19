---
name: architectural-exploration
description: Test multiple function families (step, Gaussian, spline, polynomial) with probes, then refine winner.
---

# Architectural Exploration Protocol

## Core Principle
The seed achieves ~0.934. Test diverse architectures with probes, then deeply refine the winner.

## Function Families

1. **Step Functions**: Piecewise constants (seed baseline)
2. **Smoothed Steps**: Step + Gaussian convolution (sigma = 0.05-0.5)
3. **Gaussian Mixtures**: sum w_i * exp(-(x-mu_i)^2/(2*sigma_i^2)), w_i >= 0, sum w_i = 1
4. **B-splines**: Piecewise polynomials with optimized knots
5. **Polynomial Bases**: Polynomials on [a,b], zero elsewhere

## Protocol

### Phase 1: Screening (iterations 1-10)
1. Call compare_architectures with all 5 families (5 probes)
2. Generate 2-3 variants in top 2 families
3. Probe all variants, evaluate best
4. If no improvement: try smoothed step functions (sigma = 0.1-0.3)

### Phase 2: Refinement (iterations 11-25)
1. Use JAX gradients to compute descent/ascent directions
2. Generate 3 variants, probe, evaluate best
3. If stuck (gradient norm < 0.001): reinitialize 30% of params

### Phase 3: Aggressive (iterations 26-30)
1. Try 2 new families: (a) rational functions, (b) trig polynomials
2. Probe all, evaluate best, submit if c2 > 0.8962799441554086

## Key Rules
- Call compare_architectures at iteration 1 and if stuck
- Use probes: 5 for screening + 2-3 per variant = efficient exploration
- Smoothed functions often beat hard steps (better numerical stability)
- JAX autodiff works on any differentiable family
