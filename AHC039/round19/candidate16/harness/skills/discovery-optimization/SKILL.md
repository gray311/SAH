---
name: discovery-optimization
description: "Point-level clustering with tight axis-aligned bounding boxes. Cluster mackerels spatially, build rectangles per cluster avoiding sardines, merge with MST, local search refinement."
---

# Point-Level Polygon Construction Strategy

## Phase 1: Point Clustering
- Read all fish coordinates from input
- Cluster mackerels using distance-based approach (threshold ~10000)
- For each cluster, compute tight axis-aligned bounding box [min_x, max_x] x [min_y, max_y]

## Phase 2: Sardine-Aware Rectangle Building
- For each cluster's bounding box, check if any sardine lies on or very near the boundary
- If a sardine is within 100 units of a boundary, expand that boundary outward
- Use binary search to find minimum expansion that excludes all boundary sardines
- Ensure all coordinates remain in [0, 100000]

## Phase 3: Polygon Merging
- Compute pairwise distances between cluster rectangles (use min distance between edges)
- Build MST connecting all rectangles
- For each MST edge, create a corridor rectangle connecting the two parent rectangles
- Ensure corridors don't contain sardines (expand if needed)

## Phase 4: Local Search Refinement
- For each edge of the final polygon, try expansions/shrinkages by ±50, ±100, ±200
- Use rectangle-based counting (not full polygon point-in-polygon) for fast scoring
- Accept changes that improve (mackerels - sardines) without violating constraints
- Run 5-10 refinement iterations

## Phase 5: Multiple Strategy Ensemble
- Try 8-12 different construction approaches:
  * Single rectangle around all mackerels
  * Per-cluster rectangles with MST connections
  * Convex hull approximation (project to axis-aligned)
  * Greedy expansion from densest region
- Output best valid polygon

## C++ Implementation Notes
- Use O(N log N) or O(N) sorting for coordinate processing
- Rectangle query: sum points in axis-aligned rectangle using 2D prefix sums or sweep line
- Total time per evaluation: < 2.0s with efficient operations
- Use fast point-in-rectangle tests instead of full polygon point-in-polygon
