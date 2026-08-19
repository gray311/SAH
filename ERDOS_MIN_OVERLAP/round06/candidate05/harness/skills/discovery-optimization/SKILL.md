---
name: discovery-optimization
description: "C\u2085 bound optimization via constructive search. Build explicit step function candidates (not gradient descent). Target combined_score > 1.0."
---

# Constructive Search for C₅ Bound

## Problem
Minimize: max_k ∫_0^2 h(x)(1-h(x+k))dx
Subject to: h:[0,2]→[0,1], ∫h=1

## Why Gradient Descent Fails
The seed's 12 random/sine initializations + Adam optimizer get trapped in local optima. 
The landscape has many suboptimal basins.

## Constructive Strategy

### Pattern 1: Single Step
h(x) = 1 for x∈[0,1], 0 elsewhere (normalized to ∫h=1)
This is a natural candidate - concentrated mass minimizes overlap with shifted versions.

### Pattern 2: Double Step
h(x) = 0.5 for x∈[0,0.5] ∪ [1.5,2], 0 elsewhere
Split the mass into two regions to reduce self-overlap.

### Pattern 3: Asymmetric Step
h(x) = 1 for x∈[0,a], 0 elsewhere, where a is optimized
Or: h(x) = c for x∈[0,a] ∪ [b,2], optimized for integral=1

### Pattern 4: Concentrated Mass
h(x) = M for x∈[0,1/M], 0 elsewhere (very narrow spike)
Tests extreme concentration hypothesis.

### Pattern 5: Symmetric Triples
Three equal steps at [0,a], [b,1], [2-b,2] for symmetry.

## Tool Usage
- **construct_solution**: Build a complete step function with specified breakpoints and values
- **evaluate_solution**: Get exact combined_score for each candidate
- **probe_solution**: NOT available (use evaluate directly)

## Execution Flow
1. Construct candidate 1 (single step) → evaluate → record score
2. Construct candidate 2 (double step) → evaluate → record score
3. Construct candidate 3 (concentrated) → evaluate → record score
4. Try variations: adjust breakpoints, try asymmetric splits
5. If any score > 0.38092303510845016, combined_score > 1.0 ✓

## Key Insight
Step functions with FEWER breakpoints may outperform the seed's 800-interval smooth approach.
The optimal h may be a simple piecewise constant, not a finely-grained smooth function.
