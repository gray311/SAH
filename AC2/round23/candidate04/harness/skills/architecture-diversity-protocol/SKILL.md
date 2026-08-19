---
name: architecture-diversity-protocol
description: C2 maximization via architecture exploration. Prioritize new function families over parameter tuning.
---

# C2 Maximizer: Architecture Diversity Protocol

## Core Principle

The seed step patterns (12 variants) form a local optimum. Parameter tuning won't escape. YOU MUST explore NEW function families: polynomials, splines, and hybrids.

## Phase 1: Function Family Diversification (iterations 1-10)

Step 1: Inspect Current Code
- Look for pattern_idx -> step-function
- Look for 'polyval' or 'exp(-' -> polynomial
- Look for 'BSpline' or 'spline' -> spline

Step 2: Generate 2 NEW Function Families
Variant A (Polynomial Decay):
- f(x) = exp(-|x|^α) for α ∈ {1.5, 2.0, 2.5}
- f(x) = (1 + x^2)^(-β) for β ∈ {1.0, 1.5, 2.0}

Variant B (Spline with Optimized Knots):
- 5-7 piecewise linear segments
- Knot positions: [0.15, 0.35, 0.55, 0.65, 0.85]

Step 3: Probe and Evaluate
- Call probe_solution on BOTH variants (2 probes)
- Evaluate TOP 1

Step 4: Iterate
- If beats record: continue in Phase 1
- If no improvement after 3 iterations: switch to Phase 2

## Phase 2: Step-Polynomial Hybrids (iterations 11-20)

Step 1: Hybrid Construction
- Keep step in center [0.25, 0.75]
- Add polynomial decay for |x| > threshold

Step 2: 3 Hybrid Variants
- Gaussian wings: exp(-(x-t)^2)
- Rational decay: 1/(1+x^2)
- Sigmoid blend

Step 3: Probe all 3, evaluate best

## Phase 3: B-Spline (iterations 21-30)

Step 1: B-Spline with 10-15 basis functions
- Optimize knot positions and coefficients

Step 2: 2 variants (uniform vs adaptive knots)

Step 3: Probe, evaluate, submit if c2 > 0.8962799441554086

## Key Rules

- ALWAYS explore NEW families - don't just tweak parameters
- Use probes to filter: 2-3 probes before full eval
- If iteration 15+ with no improvement: call edit_solution for new function class
- Budget: 30 probes - spend on diverse architectures
