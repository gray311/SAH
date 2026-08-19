---
name: coarse-fine-c5-search
description: Method for escaping local optima in C5 bound optimization. Key insight - Gradient descent on fine discretizations gets stuck. Solution - Start coarse (50-100 intervals), find good pattern, then refine. Also try explicit combinatorial structures with few breakpoints.
---

# Coarse-to-Fine Strategy for C5 Optimization

## Core Principle

The C5 minimization problem has a highly non-convex landscape. 
Gradient-based optimization on 800-point discretizations finds local optima
that are far from the global optimum.

## Three-Phase Approach

### Phase 1: Coarse Exploration (50-100 intervals)

- Use num_intervals = 50-100
- Increase penalty_strength to 5000-10000 to enforce integral constraint
- Use simpler, more structured initializations
- Goal: Find a pattern that beats the seed (combined_score > 0.999641)

### Phase 2: Structural Refinement

- Once you have a beating pattern, systematically vary:
  * Breakpoint positions
  * Region heights (must stay in [0,1])
  * Number of regions (2, 3, 4, 5, 6)
- Use the probe tool to quickly rank variants
- Goal: Improve the coarse solution by 5-10%

### Phase 3: Fine Discretization

- Gradually increase intervals: 100 -> 200 -> 400 -> 800
- Preserve the discovered pattern structure
- Use transfer learning: initialize fine solution from coarse optimum
- Goal: Extract as much precision as possible from the coarse pattern

## Alternative: Explicit Combinatorial Search

Instead of gradient descent, enumerate specific structures:

1. Single step: h=1 on [0,1], 0 elsewhere
   - This is valid (integral=1) but gives poor C5 bound
   
2. Double step: h=a on [0,b], h=c on [d,2], h=0 elsewhere
   - Vary a, b, c, d to minimize overlap
   - Symmetric: b = d-1
   - Asymmetric: explore all configurations

3. Periodic patterns: 
   - h(x) = f(x mod p) for small period p
   - Easy to parameterize and optimize

## Implementation Checklist

[ ] Start with 50 intervals, penalty=5000
[ ] Try 3-4 explicit step function structures
[ ] Use probe to rank before full evaluation
[ ] Refine best structure to 100+ intervals
[ ] Only then explore 200+ intervals
[ ] Document which structure type works best
