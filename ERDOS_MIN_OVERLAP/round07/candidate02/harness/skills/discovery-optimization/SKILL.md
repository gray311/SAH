---
name: discovery-optimization
description: "Erdos C5 bound optimization. Uses structural constructions (piecewise constant, Fourier-based) to escape local optima. Requires combined_score > 1.0."
---

# Erdos C5 Bound: Structural Construction Strategies

## Problem
Minimize: max_k integral from 0 to 2 of h(x)(1-h(x+k)) dx
Subject to: h:[0,2]->[0,1], integral from 0 to 2 of h(x) dx = 1

## Why Gradient Descent Fails
The seed's 59K-step Adam optimizer finds local optima. The landscape is non-convex with many plateaus.

## STRATEGY 1: Piecewise Constant with Strategic Breakpoints

Try these EXACT patterns (implement directly, not random):

Pattern A: Uniform on [0.5, 1.5]
- h = 1 if x in [0.5, 1.5], h = 0 otherwise
- Integral: 1.0 exactly
- This is symmetric and simple

Pattern B: Two intervals [0, 0.5] and [1.5, 2]
- h = 1 if x in [0, 0.5] U [1.5, 2], h = 0 otherwise
- Integral: 0.5 + 0.5 = 1.0

Pattern C: h = 1 on [0, 1], h = 0 on [1, 2]
- Integral: 1.0

## STRATEGY 2: Sparse Concentrated Functions

Critical insight: h=1 on a single interval of length 1 satisfies integral=1.
The overlap integral for shift k: integral h(x)(1-h(x+k)) dx

## STRATEGY 3: Gradient Refinement (Last Resort)

Only after trying structural constructions:
- Start with num_intervals = 50 (coarse)
- Use num_steps = 5000, not 59000
- Use multiple seeds and pick best

## Execution Order
1. Implement h=1 on [0.5, 1.5], h=0 elsewhere, evaluate (1 eval)
2. Implement double-interval variants, evaluate
3. If none beat 0.3809, try gradient with coarse intervals
4. Report which construction worked best
