---
name: discovery-optimization
description: "Multi-cluster corridor search finds disjoint high-density clusters, connects with minimal-perimeter corridors, then refines with hill climbing using 200x200 grid."
---

# Multi-Cluster Corridor Polygon Optimization

## Phase 1: Cluster Discovery
Grid: 200x200 cells, cell_size=500, over 0-100000 by 0-100000
Score each cell: mackerels - sardines
Extract top 20 cells
Group adjacent cells into super-clusters

## Phase 2: Local Refinement
For each super-cluster:
  - Create tight bounding box
  - Add 1-2 directional protrusions (N,S,E,W)
  - Keep top 2 variants

## Phase 3: Corridor Connection
For each pair of top 10 super-clusters:
  - Connect with straight line between centers
  - net_score = mackerels_added - sardines_added - 0.001*2*distance
  - Keep if net_score > 0.1

## Phase 4: Hill Climbing
For best polygon:
  - Try edge shifts of +/- 5, +/- 10, +/- 15 units
  - Use grid scoring
  - Repeat 2 rounds

## Phase 5: Restarts
Run Phases 1-4 with 3 seeds, keep best

## Notes
Grid construction: O(N)
Cell query: O(1) with prefix sums
Total time: < 1.8s
