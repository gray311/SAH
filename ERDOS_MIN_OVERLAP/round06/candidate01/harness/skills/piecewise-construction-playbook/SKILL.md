---
name: piecewise-construction-playbook
description: Method for constructing piecewise constant extremal functions for the Erdős C₅ problem. Build explicit candidates with few breakpoints instead of gradient search.
---

# Piecewise Construction for C₅ Bound

## Core Principle

The optimal step function h for minimizing max_k ∫h(x)(1-h(x+k))dx is piecewise constant
with FEW breakpoints (typically 2-5 regions). Don't use 800-dimensional gradient search.

## Construction Templates

### 1-Segment (Uniform)
h(x) = 0.5 for x ∈ [0,2]
- Integral: 0.5 * 2 = 1 ✓
- Simple baseline

### 2-Segment Split
h(x) = a for x ∈ [0,t], h(x) = b for x ∈ [t,2]
- Constraint: a*t + b*(2-t) = 1
- Try: t=1, (a,b) ∈ {(1,0), (0,1), (0.5,0.5), (0.6,0.4)}

### 3-Segment Patterns (Most Promising)

**Pattern A: Concentrated mass**
h = [1, 0, 1] on [0,t1], [t1,t2], [t2,2]
- Try t1=1/3, t2=2/3: h=1 on [0,1/3]∪[2/3,2], h=0 on [1/3,2/3]
- Integral: 1*(1/3) + 0*(1/3) + 1*(4/3) = 5/3 ≠ 1 → scale down

**Pattern B: Symmetric dip**  
h = [1, 0, 1] centered around x=1

**Pattern C: Bipartite**
h = [a, b] on [0, t], [t, 2] with a ≠ b

## Evaluation Protocol

For each candidate:
1. Verify: h ∈ [0,1] everywhere, ∫h = 1
2. Compute c5_bound via FFT correlation
3. Calculate combined_score = 0.38092303510845016 / c5_bound
4. If combined_score > 1.0, SUCCESS!

## Search Strategy

1. Start with 3-5 simple configurations
2. Use construct_piecewise tool to evaluate each
3. Systematically vary:
   - Number of segments: 2, 3, 4, 5
   - Breakpoint locations: equal spacing, clustered, symmetric
   - Height assignments: monotonic, bipartite, uniform
4. If a candidate scores well, try refining with more segments

## Expected Results

- Simple uniform (h=0.5): likely c5_bound ≈ 0.38 (score ≈ 1.0)
- Concentrated mass patterns: may achieve c5_bound < 0.38 (score > 1.0)
- The key is breaking symmetry and concentrating h in strategic regions
