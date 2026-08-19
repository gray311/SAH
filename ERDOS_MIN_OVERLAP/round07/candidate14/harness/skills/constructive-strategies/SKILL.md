---
name: constructive-strategies
description: Concrete mathematical construction methods for the Erdős C₅ problem. Use these to generate starting candidates instead of relying solely on gradient descent.
---

# Constructive Strategies for Erdős C₅

Goal: Find h:[0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1-h(x+k))dx

## Strategy 1: Single Peak with Scaling

- Set h=1 on [0, L], h=0 elsewhere
- Choose L=1 to get ∫h=1 automatically
- This gives a baseline, but may not be optimal

## Strategy 2: Two Equal Peaks

- Set h=0.5 on [0, 0.5] and [1.5, 2], h=0 elsewhere
- This spreads mass and might reduce overlap

## Strategy 3: Uniform with Strategic Gap

- Set h=1 on [0, 0.5], h=0 on [0.5, 1.5], then something on [1.5, 2]
- The gap might reduce correlations at certain lags

## Strategy 4: Triple Symmetric Peaks

- Three equal peaks spread across [0,2]
- Symmetry might help reduce the maximum overlap

## Strategy 5: Concentrated Mass

- Very concentrated h might have higher self-overlap
- Try concentrated h on one region to understand the tradeoff

## Implementation Pattern

When editing EVOLVE-BLOCK:
1. Try num_intervals=50,100,200,500,800 sequentially
2. Use generate_candidate to test constructions quickly
3. For promising candidates, convert to a fixed initialization
4. Only then run the Adam optimizer to fine-tune

## Key Metric

Track: combined_score = 0.38092303510845016 / c5_bound
Target: combined_score > 1.0 (i.e., c5_bound < 0.38092303510845016)
