---
name: discovery-optimization
description: "Cluster-based axis-aligned polygon optimization. Parse fish coordinates, cluster mackerels spatially, build bounding boxes around clusters, explicitly count sardines inside each, hill climb edges, try multi-rectangle unions. Time <1.95s."
---

# Cluster-Based Polygon Construction Strategy

## Phase 1: Coordinate Extraction
- Parse input to extract all mackerel coordinates (type=1) and sardine coordinates (type=-1)
- Store in separate vectors for O(1) access

## Phase 2: Spatial Clustering
- For each mackerel, check for other mackerels within 5000 units (Euclidean distance)
- Use simple BFS/DFS to group connected mackerels into clusters
- Track cluster representative (centroid or extreme points) and member count

## Phase 3: Bounding Box Construction
For each cluster:
- Find min_x, max_x, min_y, max_y among cluster members
- Build axis-aligned rectangle [min_x, max_x] × [min_y, max_y]
- Verify perimeter = 2*(max_x-min_x + max_y-min_y) <= 400,000

## Phase 4: Sardine Audit
For each rectangle:
- Count sardines inside: iterate all sardines, check if min_x <= s.x <= max_x and min_y <= s.y <= max_y
- Points on boundary count as inside
- Score = cluster_mackerels - sardines_inside + 1

## Phase 5: Edge Hill Climbing
For each polygon edge:
- Try extending edge outward by ±10, ±20, ±30 units
- Recompute sardine count for each variant
- Keep change that increases score
- Repeat 2 refinement rounds

## Phase 6: Multi-Rectangle Strategy
- Consider combining 2-3 disjoint rectangles
- Total score = sum of individual rectangle scores
- This can capture separated mackerel clusters

## Phase 7: Output
- Convert final rectangle(s) to polygon vertex format
- Output: number of vertices, then vertices (clockwise or counter-clockwise)

## Implementation Notes
- Use fast point-in-rectangle test
- Total time per evaluation must be < 1.95 seconds
- Handle edge cases: empty clusters, single mackerel, all mackerels in one cluster
