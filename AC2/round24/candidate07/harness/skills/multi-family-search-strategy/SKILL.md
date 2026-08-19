---
name: multi-family-search-strategy
description: Explore multiple function families (steps, Gaussians, splines, hybrids) to escape local optima. Change families when step search exhausts.
---

# Multi-Family Function Search for C2 Maximization

## Core Strategy
AlphaEvolve reached 0.89628 with step functions, but the global maximum may lie in smoother or hybrid functions.
This playbook explores multiple families systematically.

## Phase 1: Scan Step Patterns (iterations 1-10)

1. Call scan_pattern_variants(pattern_indices=[0,1,2,...,11]) to explore all 12 seed step patterns
2. Identify the top 3 patterns by complexity (higher complexity = more optimization parameters)
3. For each top pattern: call evaluate_solution with the seed's _optimize function (JAX gradient descent)
4. If best <= seed score: immediately switch to Phase 2 (step search is exhausted)

## Phase 2: Gaussian & Spline Families (iterations 11-20)

### Gaussian Mixtures
- f(x) = Sum w_i * exp(-(x-mu_i)^2/(2*sigma^2)) where Sum w_i = 1
- Start with 2-Gaussian symmetric: centers at +/-mu, weights [0.5, 0.5], shared sigma
- Optimize mu, sigma, and weights with JAX
- Try k=3,4,5 for richer structure

### Spline Functions
- Piecewise linear with k=5-10 breakpoints
- Optimize breakpoint positions and segment heights
- Ensure continuity for smoothness

### Hybrid Functions
- f(x) = (1 - smooth_factor) * step_function + smooth_factor * gaussian
- Use tanh for smooth transitions: tanh(alpha * (x-x0))

## Phase 3: Multi-Scale Hybrids (iterations 21-30)

1. Multi-resolution: coarse step skeleton + fine smooth details
2. Fourier-constrained optimization
3. Try completely different kernel families

## Tool Usage
- scan_pattern_variants: Call once at start to unlock step search space
- probe_solution: Call on 3-5 variants per family
- evaluate_solution: Call on TOP 1 per family
- Switch families immediately if current family exhausts
