---
name: c5-pattern-search
description: Use discrete pattern generation to find step functions minimizing C5 bound. Prioritize combinatorial constructions over gradient-based optimization.
---

# C5 Pattern Search Method

## Overview
This skill guides you to find better C5 bounds by directly constructing
step function patterns rather than relying on gradient descent.

## Why This Works
The Erdos minimum overlap problem has discrete optimal solutions (step
functions with few jumps). Gradient-based methods get stuck in local
optima because they're designed for smooth, continuous landscapes.

## Core Strategy

### 1. Pattern Generation
Use gen_step_function to create diverse candidates:
- two_step: Single block h=1 on [0,1]
- three_step_symmetric: Two blocks, symmetric around x=1
- five_step: Alternating pattern with three active regions
- waveform: Sinusoidal pattern smoothed through sigmoid
- concentrated: Narrow high-amplitude peaks

### 2. Pattern Evaluation
For each candidate:
- Verify constraints: h in [0,1], integral(h)=1
- Compute c5_bound = max_k integral h(x)(1-h(x+k))dx
- Calculate combined_score = 0.380923 / c5_bound

### 3. Pattern Mutation
Mutate top patterns:
- Shift intervals: Move active regions left/right
- Change widths: Vary interval sizes while maintaining integral(h)=1
- Add/remove steps: Increase/decrease number of jumps
- Combine patterns: Blend features of multiple good patterns

### 4. Brief Optimization
For promising patterns (combined_score close to 1.0):
- Run short gradient descent (100-500 steps)
- Re-evaluate after optimization
- Compare to original pattern

## Checklist for Each Iteration
- [ ] Generate 3-5 patterns via gen_step_function
- [ ] Evaluate all patterns
- [ ] Record best pattern and its combined_score
- [ ] If combined_score > 1.0: SUCCESS, finish with summary
- [ ] If no success: mutate top 2 patterns for next iteration
- [ ] Use budget wisely: ~5 evals for pattern exploration, ~5 for refinement

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- At least one pattern with c5_bound < 0.35
- Multiple patterns with c5_bound between 0.35-0.38
- Identify the best pattern type for this problem

## Common Pitfalls
- Relying solely on gradient descent (won't find right pattern)
- Not checking integral constraint after modifications
- Using too many optimization steps (wastes budget)
- Not exploring diverse pattern types
- Ignoring symmetric patterns (often optimal for this problem)
