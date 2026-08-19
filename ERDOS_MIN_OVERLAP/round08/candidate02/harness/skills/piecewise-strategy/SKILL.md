---
name: piecewise-strategy
description: Use piecewise constant constructions for C5 optimization. Generate explicit candidates with few breakpoints, then evaluate. Do not rely on gradient descent over 800 parameters.
---

# Piecewise Strategy for C5 Bound Optimization

PROBLEM RECAP

Minimize: max over k of integral from 0 to 2 of h(x)(1-h(x+k)) dx
Subject to: h maps [0,2] to [0,1], integral of h equals 1

WHY PIECEWISE WORKS

The optimal solution is structurally simple: a few rectangular blocks.
Parameterizing with 800 continuous values wastes the search budget.

CONSTRUCTION RECIPES

SINGLE BLOCK (baseline)
h(x) equals 1 if x is in [0,1], else 0
This satisfies integral=1 by construction.

DOUBLE BLOCK (spread mass)
h(x) equals 0.5 if x is in [0,0.5] union [1.5,2], else 0
Spreads the mass to reduce overlap with shifted copies.

THREE BLOCK (more spread)
h(x) approximately equals 1/3 on three intervals of length 2/3 each
Even more spreading, potentially better overlap.

SYMMETRIC PATTERNS
Center blocks around x=1 to exploit symmetry in the overlap integral.

ASYMMETRIC PATTERNS
Break symmetry to explore different regions of the solution space.

EVALUATION WORKFLOW

1. Generate 5-10 candidates using construct_candidates
2. Evaluate each to get c5_bound
3. Identify patterns that work
4. Refine by adjusting breakpoint positions
5. Consider hybrid: piecewise structure with gradient refinement

KEY INSIGHT

STRUCTURAL SIMPLICITY BEATS PARAMETRIC FLEXIBILITY.
The answer to how to minimize max overlap is likely to spread the mass
into few rectangular chunks, not to optimize 800 independent values.

WHEN TO USE

- Always at the start: generate diverse piecewise candidates
- When gradient descent stalls: try explicit construction
- When combining: use piecewise to initialize latent optimization
