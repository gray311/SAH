---
name: discovery-optimization
description: "Generate diverse step-function candidates for Erdos optimization.\n\nCall generate_single_candidate once per iteration.\nVerify integral=1.0. Call probe_solution for fast screening."
---

# Erdos Optimization Method

## Objective
Minimize C5 = max_k integral(h(x)(1-h(x+k)))dx over [0,2]

## Constraints
1. h(x) in [0,1]
2. integral(h) = 1.0 exactly

## Candidate Generation Strategy

Use structured patterns, not random noise:

1. **Bipartite patterns**: Two separated regions of h=1
   - Example: h(x)=1 for x in [0,1] U [1.5,2], 0 otherwise
   - This gives integral=2, so scale to get integral=1

2. **Tri-modal patterns**: Three narrow peaks
   - Place peaks at optimal spacing to minimize overlap
   - Spacing: ~0.4 between peak centers

3. **Golomb ruler patterns**: Peaks at positions with minimal pairwise distances
   - Classic Golomb ruler positions: [0,1,3,6] normalized to [0,2]

## Validation Checklist

Before calling evaluate_solution:
- integral(h) must be exactly 1.0 (within 0.001 tolerance)
- max(h) must be <= 1.0
- min(h) must be >= 0.0

## Editing Strategy

When improving a candidate:
1. Identify the interval with highest overlap contribution
2. Try shifting it left/right by 0.05-0.1
3. Try splitting a wide peak into two narrower peaks
4. Try merging two adjacent narrow peaks into one
5. Always re-normalize to maintain integral=1.0

## Probing Strategy

- Use probe_solution (500 intervals) for fast screening
- If c5_approx < 0.38, do full evaluation
- If c5_approx >= 0.38, discard and generate new candidate

## Budget Management

- Max 30 full evaluations
- Use probe to filter before full eval
- Refine ONE good candidate before exploring new ones
