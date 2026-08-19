---
name: discovery-optimization
description: "Systematically scan diverse function representations using probes before full evaluation. Enforce scan-refine protocol: 3-4 representations x 3-5 probes each, then refine top 2-3 with full evaluations. Diversify early, do not tunnel."
---

# C2 Function Discovery Protocol

## Objective
Maximize C2 = ||f convolve f||_2^2 / ((int f)^2 ||f convolve f||_inf) > 0.8963

## Protocol: Scan then Refine

### Phase 1: Representation Scan (~18 probes)
Test 4+ function classes, 3-5 probes each:

A. Step Functions (Piecewise-Constant)
- Current record-holder (0.8963)
- Vary: support width, levels, symmetry
- Probe: wide/narrow/symmetric/asymmetric variants

B. Piecewise-Linear (Current Seed)
- Vary: intervals (100, 200, 300)
- Probe: different initialization patterns

C. Gaussian Mixtures
- Parameterize: means, variances, weights
- Probe: 2/3/5 components

D. Exponential Combinations
- Form: sum w_i * exp(-alpha_i * |x - mu_i|)
- Probe: single/double exponential

### Phase 2: Refinement (~4-5 full evals)
For top 2-3 representations:
1. Increase intervals/parameters by 2-3x
2. Multi-start: 3 random initializations each
3. Fine-tune: LR, steps, stagnation

### Phase 3: Ensemble and Innovation
- Weighted averages
- Analyze structural properties
- Design inspired variants

## Best Practices
- Probe FIRST: 3-5 probes per representation
- Diversify early: Test 4+ representations
- Reserve evals: 4-5 full evaluations for promising variants
- Validate: f(x) >= 0, int f > 0

## Recovery
- If stuck: Try different function class
- If evals low: Consolidate on best
- If errors: Fix immediately
