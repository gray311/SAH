---
name: mathematical-construction
description: Method playbook for constructing step functions in the Erdős minimum overlap problem. Use when trying to beat the current best bound. Focus on explicit, deterministic constructions.
---

# Mathematical Construction Guide for Erdős Minimum Overlap

## Core Idea
Find h: [0,2]→[0,1] with ∫h=1 minimizing max_k ∫h(x)(1-h(x+k))dx.

## Construction Patterns to Try

### Pattern A: Binary Step (Simple)
h(x) = 1 for x ∈ [0, 1], h(x) = 0 for x ∈ (1, 2]
- This is a pure step function
- Compute the overlap integrals explicitly
- Modify: create [a,b] and [c,d] steps to optimize

### Pattern B: Alternating Steps
Divide [0,2] into n equal segments, alternate heights a and b:
- Ensure: (n/2)*a*(2/n) + (n/2)*b*(2/n) = 1  →  (a+b)*2/n = 1
- Choose a,b to minimize the max overlap
- Try: a=0.8, b=0.4; or a=0.9, b=0.2

### Pattern C: Three-Level Function
h(x) takes values from {0, 0.5, 1}
- Easy to compute overlap analytically
- Try: 1/4 at height 1, 1/2 at height 0.5, 1/4 at height 0

## Optimization Workflow

1. **Start Simple**: Use 50-100 intervals, 3-5 steps
2. **Validate Constraint**: Ensure ∫h=1 exactly
3. **Compute Overlap**: Use FFT for fast correlation
4. **Perturb**: Move steps, change heights, maintain constraint
5. **Refine**: Use gradient descent for final tuning

## Key Insight
The optimal h likely has LOCALIZED "high" regions separated by "low" regions.
Think of h as placing "mass" in strategic locations to minimize pairwise overlap.

## Warning
Don't use complex continuous functions - they're harder to optimize.
Start with explicit step functions, then smooth if needed.
