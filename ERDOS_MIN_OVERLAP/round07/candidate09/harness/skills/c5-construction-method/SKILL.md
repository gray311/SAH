---
name: c5-construction-method
description: Method for constructing step functions that minimize max_k ∫ h(x)(1-h(x+k))dx. Each construction provides a candidate h that satisfies integral=1 and h∈[0,1].
---

# C₅ Construction Methods

## Mathematical Background

We minimize: max_k ∫_0^2 h(x)(1-h(x+k))dx
subject to: h:[0,2]→[0,1], ∫_0^2 h = 1

The key insight: spread h(x) and h(x+k) to minimize overlap.

## Construction 1: Single Interval (Baseline)

h(x) = 1 for x ∈ [0,1], 0 otherwise
- Integral: 1 ✓
- c5_bound ≈ 0.5
- combined_score ≈ 0.76

Implementation: Large positive latent on [0,1], large negative elsewhere.

## Construction 2: Two Symmetric Humps

h(x) = 0.5 for x ∈ [0,0.5] ∪ [1.5,2], 0 elsewhere
- Integral: 0.5×0.5 + 0.5×0.5 = 0.5 (double to get 1)
- Better spreads h(x) across domain
- Target: c5_bound ≈ 0.35

Implementation: Two regions with large positive latent.

## Construction 3: Three-Interval Pattern

h(x) = 1 on [0,0.5] ∪ [1,1.5], 0 on [0.5,1] ∪ [1.5,2]
- Integral: 0.5 + 0.5 = 1 ✓
- More spread reduces peak correlations
- Target: c5_bound ≈ 0.33

Implementation: Alternating high/low latent regions.

## Construction 4: Optimized Multi-Step

Use 4-6 step intervals, optimize both positions and heights.
Start coarse (100 intervals), refine to 500+.

## Optimization Tips

1. **Lower penalty_strength**: 1370 → 200-600 allows more flexible h
2. **More restarts**: 3 → 5-10 increases chance of good initialization
3. **Coarse start**: 100 intervals, then increase after good solution
4. **Fewer steps**: 59000 → 10000-30000 avoids overfitting
5. **Larger learning rate**: 0.0053 → 0.008 for faster escape from bad regions

## Step-by-Step Execution

1. Generate 5 candidates using different constructions
2. Probe each to rank (cheap evaluation)
3. Evaluate top 2-3 candidates fully
4. Refine winner with more intervals and tuned parameters
5. Repeat with new constructions if needed

**Goal**: combined_score > 1.0 (c5_bound < 0.3809)
