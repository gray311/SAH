---
name: discovery-optimization
description: "Optimizing C++ geometric construction programs. Use probe_solution for rapid variant ranking, then confirm promising candidates with evaluate_solution. Focus on bounding boxes, iterative refinement, and efficient internal search loops."
---

# Geometric Packing Optimization Strategy

## Phase 1: Understand the Data
- The task has N=5000 mackerels and N=5000 sardines at integer coordinates [0, 100000].
- Score = max(0, mackerels_in_polygon - sardines_in_polygon + 1).
- Polygon must be axis-aligned, non-self-intersecting, ≤ 1000 vertices, perimeter ≤ 400,000.

## Phase 2: Strategy Selection
Start with a bounding box strategy:
1. Find the bounding box of mackerels with high density.
2. Compute initial polygon (likely a rectangle or L-shape).
3. Use probe_solution to test variants quickly.
4. Iteratively refine: cut off corners that contain sardines, expand where mackerels are dense.

## Phase 3: Iterative Refinement
For each refinement step:
1. Generate 3-5 variants (small shifts, corner cuts, different orientations).
2. Use probe_solution to rank them on subsampled data.
3. Evaluate top 1-2 variants with evaluate_solution.
4. Keep the best, repeat.

## Phase 4: Time Management
- Per-evaluation time limit is ~1.95 seconds (safety margin 0.05s from 2.0s).
- Ensure C++ code's internal search completes well within this limit.
- If approaching timeout, reduce search iterations or switch to simpler construction.

## Phase 5: Validation
- Check polygon validity: non-self-intersecting, correct vertex count, perimeter within budget.
- A score of 0 likely means invalid polygon or timeout.

## Tool Usage
- Always call probe_solution FIRST when testing new construction ideas.
- Only call evaluate_solution when probe scores suggest a candidate is promising.
- When evaluations_left is low, make each count: refine only the best direction.
