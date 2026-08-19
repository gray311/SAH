---
name: discovery-optimization
description: "C5 bound optimizer using targeted step-function constructions with gradient refinement.\nFocus on symmetric patterns, multi-level steps, and periodic constructions."
---

# C5 Bound Optimization: Targeted Construction Strategy

## Problem
Minimize max_k int_0^2 h(x)(1-h(x+k))dx over h:[0,2]->[0,1] with int h=1.

Current best: 0.38092303510845016 (C5 <= this value)

## Why Standard Gradient Descent Fails

The objective is non-convex with many local optima. Random initializations get trapped.
We need STRATEGIC constructions, not blind optimization.

## Recommended Constructions (Try in Order)

### Construction 1: Symmetric 3-Level (Baseline to beat)
h = 1.0 on [0, 0.5] and [1, 1.5], h = 0 elsewhere
- Expected c5_bound: ~0.375
- Action: Start here, then perturb intervals

### Construction 2: Split Single Block
h = 1 on [a, b] where (b-a) = 1
- Try: [0,1], [0.25, 1.25], [0.5, 1.5], etc.
- Shift to reduce self-overlap

### Construction 3: Triangular Wave
h(x) = 2x for x in [0, 0.25], h(x) = 0.5 for x in [0.25, 0.75],
       h(x) = 1-2x for x in [0.75, 1.0], mirrored on [1,2]

### Construction 4: Cosine Symmetric
h(x) = C * (1 + cos(pi * (x-1))) for x in [0,2], scaled to integral=1

### Construction 5: Three-Step Asymmetric
h = a1 on [0, w1], a2 on [0.5, 0.5+w2], a3 on [1, 1+w3]
Choose a1,a2,a3,w1,w2,w3 to minimize overlap

## Execution Protocol

1. For each construction:
   - Set num_intervals = 200
   - Initialize h discretely as specified
   - Optimize for 1000-2000 steps with Adam (lr=0.01, penalty=10000)
   - Record c5_bound

2. If c5_bound < 0.38:
   - Try num_intervals = 800 with same initialization
   - Try different optimizer settings (lr=0.001, steps=10000)

3. If stuck at same score:
   - Try a DIFFERENT construction from the list
   - Do NOT spend 20 evals refining one construction

4. Success criterion: combined_score > 1.0

## Important

- Each evaluation is ~10-30 seconds
- You have ~30 evaluations total
- Diverse exploration beats deep refinement when starting from seed
- The seeds multi-pattern initialization is too random; use STRUCTURED starts
