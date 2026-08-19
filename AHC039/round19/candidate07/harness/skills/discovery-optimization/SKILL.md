---
name: discovery-optimization
description: "Fine-grained vertex-level optimization. Identify mackerel clusters, build initial rectangles, optimize vertices with \u00b11..3 shifts, combine adjacent clusters, local search with edge flips, 5-8 restarts."
---

# Fine-Grained Vertex Optimization Strategy

## Phase 1: Cluster Detection
- Find dense regions of mackerels (points within 500-1000 unit radius)
- Use KD-tree or grid for efficient nearest-neighbor queries
- For each cluster of size >= 5, compute minimal bounding box

## Phase 2: Initial Polygon Construction
- For each cluster, create a 4-vertex axis-aligned rectangle covering the bounding box
- Ensure perimeter <= 400,000 and vertices in [0,100000]

## Phase 3: Vertex-Level Optimization (Key Innovation)
- For each vertex (up to 1000):
  * Try shifts: +1, -1, +2, -2, +3, -3 units in x and y directions (4 neighbors each = 24 candidates)
  * For each candidate, use fast rectangle query to compute (mackerels - sardines)
  * Keep shift that maximizes the score
- Repeat 2 refinement rounds

## Phase 4: Multicluster Combination
- After optimizing individual clusters, identify adjacent clusters (within 200 units)
- Try merging them by sharing edges or creating connecting corridors
- Use dynamic programming to select best combination of 2-5 clusters

## Phase 5: Local Search
- For the best polygon:
  * Try flipping edges (change from horizontal to vertical where possible)
  * Try vertex reordering to form more compact shapes
  * Try small expansions into empty regions if they capture additional mackerels

## Phase 6: Multiple Restarts (Optimized)
- Run 5-8 restarts with different seeds
- Each restart: pick 2-3 random mackerel clusters, build and optimize polygons
- Track best polygon across all restarts

## Implementation Notes
- Use KD-tree for O(log N) nearest-neighbor queries
- Implement fast rectangle query: sum of fish in [x1,x2]x[y1,y2] in O(1) with 2D prefix sums
- Total time per evaluation: < 2.0s
- Use std::random_device for seed generation
