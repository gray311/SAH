---
name: step-function-optimization
description: Combinatorial approach for C5 bound. Focus on few-breakpoint step functions rather than gradient descent on 800 dimensions.
---

# C5 Bound: Step Function Optimization

## Key Insight
The optimum is likely a step function with FEW breakpoints, not a complex
high-dimensional surface. Gradient descent gets trapped.

## Construction Patterns

### Pattern A: Binary
h = 1 on [0,1], h = 0 elsewhere (satisfies integral=1)

### Pattern B: Two-Value
Split [0,2] into regions with values a,b where a*l1 + b*l2 = 1

### Pattern C: Symmetric
[0, 1-p]: a, [1-p, 1+p]: b, [1+p, 2]: a

### Pattern D: Boundary
Most mass near x=0 or x=2

## Protocol

1. Call construction_prober for 100-500 candidates
2. Choose 2-3 diverse types
3. Implement each in EVOLVE-BLOCK (complete rewrite)
4. Evaluate each
5. Iterate on best type

## Important
- Simple constructions: few breakpoints, clear values
- Always satisfy integral=1
- Goal: c5_bound < 0.380923 for combined_score > 1.0
