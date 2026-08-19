---
name: discovery-optimization
description: "Simple greedy expansion with KD-tree queries, local hill climbing, 3-5 restarts."
---

# Simplified Polygon Optimization Strategy

## Phase 1: Input and Setup
- Read N mackerels and N sardines from stdin
- Store as Point structs with fish types

## Phase 2: KD-Tree Construction
- Build KD-tree on all fish points (both mackerels and sardines)
- Use KD-tree for efficient O(log N) range sum queries

## Phase 3: Initial Polygon
- Compute centroid of all mackerels
- Create minimal rectangle: [centroid.x-500, centroid.y-500] to [centroid.x+500, centroid.y+500]
- Or use bounding box of top 100 mackerels

## Phase 4: Greedy Edge Expansion
- For each of the 4 sides, try expanding outward by d ∈ {1, 5, 10} units
- Query rectangle score using KD-tree
- Keep expansion if score improves
- Stop after 50 total expansion attempts

## Phase 5: Local Refinement
- For each vertex, try perturbing by ±2, ±5, ±10 units
- Query score, keep improvement
- Repeat up to 10 iterations

## Phase 6: Multiple Restarts
- Run 3-5 restarts with different starting seeds
- Each restart: random centroid perturbation
- Output best polygon

## Validation
- Ensure 4 <= vertices <= 1000
- Ensure perimeter <= 400,000
- Ensure all coords in [0, 100000]
- Use simple self-intersection check (O(n²) is fine for n=1000)

## C++ Implementation Tips
- Use fast I/O (cin.tie(NULL), ios_base::sync_with_stdio(false))
- KD-tree query: sum of mackerels - sum of sardines in rectangle
- Score = max(0, mackerels - sardines + 1)
- Keep time < 2.0s by limiting iterations
