---
name: geometry-optimization
description: Method for NP-hard polygon construction to maximize (mackerels - sardines). Guides the executor to build parametric solutions with internal search.
---

# Geometry Optimization Strategy

## Core Insight
This is a coverage problem: cover dense mackerel regions while minimizing sardine overlap.

## Pattern 1: Cluster-Based Construction
1. Identify mackerel clusters (dense regions via grid/KD-tree)
2. Build minimal axis-aligned bounding boxes around each cluster
3. Merge adjacent boxes if perimeter budget allows
4. Refine: expand boxes toward nearby mackerels, shrink toward sardines

## Pattern 2: Greedy Expansion
1. Start with polygon containing the densest mackerel point
2. Iteratively add vertices in directions with best mackerel density
3. Stop when perimeter limit reached or score stops improving

## Pattern 3: Iterative Refinement
1. Start with simple rectangle covering all mackerels
2. Try cutting out sardine-heavy regions (subtract rectangles)
3. Or merge sub-rectangles to cover multiple clusters

## Pattern 4: Parameterized Search
1. Define a family of polygons with tunable parameters
2. Run internal search over parameters within per-test-time limit
3. Report best parameter set as vertex coordinates

## Implementation Tips for C++
- Use KD-tree for fast neighbor queries
- Precompute grid densities for O(1) cluster lookup
- Use a simple random-seed-controlled search (fixed seeds for reproducibility)
- Cache repeated computations across internal iterations
- Track best score throughout internal search

## Common Pitfalls
- Too complex: internal search may hit time limit
- Too simple: won't achieve good coverage
- Invalid polygons: ensure perimeter ≤400,000 and non-intersection
- Wrong scoring: remember score = max(0, mackerels - sardines + 1)

## Evaluation Strategy
- Use probe_solution to test algorithm variations on subsample
- Track which strategies beat baseline in probe scores
- Only run full evaluation on promising strategies
- If score doesn't improve in 5 iterations, change algorithm fundamentally
