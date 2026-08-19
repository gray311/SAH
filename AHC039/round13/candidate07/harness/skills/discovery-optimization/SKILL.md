---
name: discovery-optimization
description: "Rectangle-based fish cluster search: identify mackerel clusters, generate bounding rectangles,\ncombine rectangles into orthogonal polygon, filter by perimeter constraint, hill climb edge positions,\n5-10 restarts with varying clustering parameters."
---

# Rectangle-Based Fish Cluster Strategy

## Phase 1: Data Parsing and Clustering
- Parse all fish coordinates from input file
- Separate mackerels (type 1) and sardines (type -1)
- Cluster mackerels: group those within distance D (e.g., 5000 units)
- Identify cluster centroids and bounding boxes

## Phase 2: Rectangle Generation
For each mackerel cluster:
- Compute tight axis-aligned bounding box [min_x, max_x] × [min_y, max_y]
- Generate candidate rectangles around cluster (slightly expanded)
- Filter: perimeter = 2*(width+height) ≤ 400,000
- Filter: all vertices in [0, 100000]

## Phase 3: Rectangle Combination
- Try combining 1-5 rectangles
- Create orthogonal polygon from union of rectangles
- Use coordinate compression or bounding box as outer frame
- Apply orthogonal polygon construction:
  * Collect all unique x and y coordinates from rectangles
  * Create grid of candidate vertices
  * Build polygon edges connecting corners
  * Simplify to minimal vertex set

## Phase 4: Score Computation
For each polygon:
- Implement orthogonal point-in-polygon test (ray casting)
- Count enclosed mackerels
- Count enclosed sardines
- Score = max(0, mackerels - sardines + 1)

## Phase 5: Hill Climbing
For each candidate polygon:
- For each edge, try shifts: ±5, ±10, ±20 units
- Keep shift improving score
- Repeat 2-3 rounds
- Track best variant

## Phase 6: Multiple Restarts
- 5-10 restarts with different parameters:
  * Vary clustering distance D: 3000, 5000, 8000
  * Vary expansion factor: 1.0, 1.1, 1.2
  * Vary max rectangles: 2, 3, 5
- Output single best valid polygon

## C++ Implementation Notes
- Use efficient spatial indexing (grid or quadtree) for counting
- O(1) point-in-polygon for orthogonal polygons
- Pre-sort fish by coordinates for fast range queries
- Total time < 2.0s with optimized algorithms
- Handle edge cases: empty clusters, single rectangles, degenerate cases
