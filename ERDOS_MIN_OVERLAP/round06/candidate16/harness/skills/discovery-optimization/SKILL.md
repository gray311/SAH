---
name: discovery-optimization
description: "C5 bound optimization via discrete pattern search. Focus on combinatorial constructions rather than gradient-based fine-tuning."
---

# C5 Bound: Discrete Pattern Search Strategy

## Problem
Minimize: max_k integral from 0 to 2 of h(x)(1-h(x+k))dx
Subject to: h:[0,2]→[0,1], integral from 0 to 2 of h(x)dx = 1

## Why Gradient Descent Fails
The seed's multi-restart Adam optimizer finds good local optima but gets trapped.
The solution requires discovering the right step pattern, not fine-tuning parameters.

## Strategy: Direct Pattern Construction

### Step 1: Generate Candidate Patterns
Use gen_step_function to create diverse step function candidates:
- Two-step: Single block of height 1 (adjusted for integral constraint)
- Three-step: Symmetric patterns with center block
- Five-step: More complex piecewise constant functions
- Waveform: sin/cos-based patterns through sigmoid
- Concentrated: Mass concentrated on narrow intervals

### Step 2: Evaluate Patterns Directly
For each candidate pattern:
1. Check constraints (integral(h)=1, h in [0,1])
2. Compute c5_bound directly using FFT-based correlation
3. Record combined_score = 0.380923 / c5_bound

### Step 3: Refine Promising Patterns
For patterns with combined_score close to or exceeding 1.0:
- Run brief gradient-based optimization (few hundred steps)
- Re-evaluate after refinement
- Keep best result

### Step 4: Iterative Pattern Discovery
Each eval iteration:
1. Generate 3-5 new patterns with gen_step_function
2. Evaluate all patterns
3. If any score > 1.0, STOP and finish with that solution
4. Otherwise, mutate top-performing patterns for next iteration

## Pattern Templates

Two-step pattern:
h = 1 on [0, 1], h = 0 elsewhere (satisfies integral(h)=1)
But can shift: h=1 on [a, a+1] for any a in [0,1]

Three-step symmetric pattern:
h = a on [0, 1], h = b on [1, 2], h = a on [2, 3] (padded)
Adjust a, b to satisfy integral(h)=1

Five-step pattern:
h = 1 on [0, 0.5] union [1, 1.5], h = 0 elsewhere
Or variations with different interval widths

## Execution Plan
1. Call gen_step_function with pattern_type=two_step, then evaluate
2. Call gen_step_function with pattern_type=three_step_symmetric, then evaluate
3. Call gen_step_function with pattern_type=five_step, then evaluate
4. Call gen_step_function with pattern_type=waveform, then evaluate
5. For best pattern, run brief optimization (num_steps=1000, lr=0.01) then re-evaluate
6. If combined_score > 1.0, finish with summary

## Critical Success Factors
- Use gen_step_function to generate diverse candidates
- Don't rely on gradient descent alone - it won't find the right pattern
- Check constraints after each pattern generation
- Stop early if you find combined_score > 1.0
