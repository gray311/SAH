---
name: discovery-optimization
description: "Maximize C\u2082 for the second autocorrelation inequality. The seed program's piecewise-linear approach is locally optimal at ~0.8963. You must explore COMPLETELY DIFFERENT function classes: step functions, Gaussian mixtures, exponential combinations, and splines. Use probes to rank representations, then full evaluations only on the top 3. Focus on STRUCTURAL CHANGES, not parameter tuning."
---

# C₂ Optimization - Break Local Optima Strategy

## Critical Understanding

The current seed program uses piecewise-linear optimization with 300 intervals. It has ALREADY converged to a local optimum (~0.8963). Your job is NOT to tune this configuration further. Your job is to REPLACE the function representation entirely.

## Phase 1: Structural Change (MANDATORY)

### Option A: Step Functions (Piecewise-Constant)
- Change the _create_initializer to return a piecewise-constant function instead of piecewise-linear
- Use 50-100 intervals with flat regions
- Try different support widths: [0.1-0.9], [0.2-0.8], [0.15-0.55], [0.25-0.75]
- Try multi-step: 2-4 steps with different heights

### Option B: Gaussian Mixtures
- Replace the optimizer with a Gaussian mixture representation
- Parameterize: means [μ₁, μ₂, ...], variances [σ₁², σ₂², ...], weights [w₁, w₂, ...]
- Ensure non-negativity: f(x) = Σ w_i * exp(-(x-μ_i)²/(2σ_i²))
- Start with K=2, then K=3, K=5

### Option C: Exponential Combinations
- f(x) = Σ w_i * exp(-α_i * |x - μ_i|)
- Simpler than Gaussians, always positive

## Phase 2: Multi-Scale Testing

For EACH new representation:
1. Test with 3-5 different parameter settings using probe_solution
2. Rank by probe score
3. If top probe score > seed score, spend 1 full evaluation on it
4. If probe scores all < seed, try a different representation (don't over-invest)

## Phase 3: Refinement

Only after finding a representation that beats the seed on probes:
- Increase intervals by 2-3x
- Use multi-start (5 different initializations)
- Fine-tune hyperparameters

## Key Rules

1. NEVER spend 2+ full evaluations on the same function representation
2. ALWAYS try at least 3 different function classes before calling finish
3. If stuck, switch function class immediately (don't keep tuning)
4. Use probes to test 10+ variants before any full evaluation
5. The seed's piecewise-linear approach is DONE exploring it
