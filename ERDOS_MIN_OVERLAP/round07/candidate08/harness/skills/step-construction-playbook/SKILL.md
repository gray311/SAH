---
name: step-construction-playbook
description: Construct explicit step functions. Use N=10-50 intervals. Direct array creation. Test simple patterns.
---

# Explicit Step Function Construction

## Problem
Minimize C5 = max_k ∫ h(x)(1-h(x+k))dx over h:[0,2]→[0,1] with ∫h=1.

## Why Gradient Descent Fails
The seed program uses 800 intervals and 59000 optimization steps. This is too much - it gets trapped in local optima on high-dimensional space.

## Solution: Explicit Construction
Build h as a piecewise constant function with FEW breakpoints (2-10).

## Core Patterns (Implement These)

### Pattern 1: Single Block
h = 2.0 on [0, 0.5], h = 0 elsewhere
∫h = 2.0 × 0.5 = 1.0 ✓

### Pattern 2: Two Separated Blocks
h = 1.0 on [0, 0.5] and [1.0, 1.5], h = 0 elsewhere
∫h = 1.0 × 0.5 + 1.0 × 0.5 = 1.0 ✓

### Pattern 3: Uniform
h = 0.5 everywhere
∫h = 0.5 × 2.0 = 1.0 ✓

### Pattern 4: Concentrated
h = 2.0 on [0.25, 0.75], h = 0 elsewhere
∫h = 2.0 × 0.5 = 1.0 ✓

## Implementation Steps

1. Set num_intervals = 30 (not 800!)
2. Define h as direct array: h[i] = height of i-th interval
3. Ensure sum(h) × dx = 1.0
4. Compute C5 via FFT (already in seed)
5. Test each pattern, report best

## Key Insight
Simple patterns with few steps often outperform optimized complex functions.
Start with 2-5 patterns, evaluate, then refine the best one.
