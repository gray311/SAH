---
name: discovery-optimization
description: "Multi-architecture search for C2 maximization. Explore step, Gaussian mixture, B-spline, and hybrid function families in parallel. Use structural innovation over parameter tuning."
---

# Multi-Architecture C2 Optimizer

## Core Principle: Structural Innovation > Parameter Tweaking

The step function local optimum (0.8962799441554086) can only be escaped by:
1. Changing function family (step → spline, step → mixture)
2. Radical parameter changes (not small perturbations)
3. Hybrid architectures (combine successful elements)

## Phase 1: Parallel Architecture Exploration (iterations 1-10)

### Step 1: Generate Architectures

Call explore_architectures. It returns 3-4 different function families:
- Arch 0: Refined step functions (different patterns from seed)
- Arch 1: Gaussian mixture (2-3 components, optimized weights/widths)
- Arch 2: B-spline (5-7 knots, polynomial pieces)
- Arch 3: Asymmetric multi-level step (inspired by seed's multi-level patterns)

### Step 2: Generate and Probe Variants

For EACH architecture:
- Generate 2 representative variants
- Probe ALL 6-8 variants (use 20-25 probes across 2-3 evals)
- Track: architecture, variant, probe score

### Step 3: Evaluate Best

Evaluate the TOP 2 variants by probe score
Select best c2 across ALL architectures

## Phase 2: Best Architecture Refinement (iterations 11-20)

Take best-performing architecture from Phase 1:

### If STEP Functions:
- Try asymmetric multi-level patterns (3-5 levels)
- Split highest peak into 2 peaks
- Try Gaussian-like tails on step function

### If GAUSSIAN MIXTURE:
- Optimize mixture weights (softplus transformation for positivity)
- Adjust component widths (wider = smoother, narrower = sharper)
- Try 2-component vs 3-component configurations

### If B-SPLINE:
- Move knot positions (focus knots where gradient is highest)
- Adjust B-spline coefficients
- Try different knot distributions (uniform vs clustered)

Generate 3 refined variants, probe all, evaluate best.

## Phase 3: Boundary Pushing (iterations 21-30)

Try extreme configurations:
1. Very narrow high peak (width < 10% of domain, height > 3.0)
2. Two narrow peaks with wide base (triangle-like)
3. Hybrid: step function with Gaussian decay tails
4. Fourier-space: optimize Fourier coefficients with positivity constraint

If no improvement in 5 iterations: switch to completely new architecture.

## Key Rules

- PARALLEL SEARCH: Never focus on one architecture > 5 iterations
- AGGRESSIVE PROBING: Use 15-20 probes to rank before any full eval
- STRUCTURAL MUTATIONS: Change function class, not just parameters
- HYBRID APPROACHES: Combine successful elements from different architectures
- REPORT: Best architecture type that achieved optimal c2
