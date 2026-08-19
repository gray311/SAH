---
name: discovery-optimization
description: "Cluster-based bounding box optimization. Group mackerels into spatial clusters, build initial bounding boxes, refine edges to exclude nearby sardines, merge overlapping boxes, run multiple restarts with local optimization."
---

# Cluster-Based Bounding Box Optimization for Axis-Aligned Polygon

## Overview
Instead of grid-based corridor expansion, this strategy directly uses mackerel positions to construct optimal axis-aligned bounding boxes with sardine exclusion.

## Phase 1: Mackerel Clustering
- Read N mackerel coordinates from input
- Use spatial hashing with cell_size 200-500 to group nearby mackerels
- Each cluster = set of mackerels within spatial proximity
- Record unique x and y coordinates for each cluster

## Phase 2: Initial Bounding Box Construction
For each cluster:
- Find min_x, max_x, min_y, max_y among cluster's mackerels
- Create rectangle with these 4 vertices (or more if cluster is irregular)
- Verify: 4 <= vertices <= 1000, coords in [0,100000], perimeter <= 400,000
- If cluster is small (< 10 mackerels), consider alternative shapes

## Phase 3: Sardine Exclusion Refinement
For each bounding box edge:
1. Collect all sardines within distance 100 of the edge
2. For each nearby sardine, calculate benefit of excluding it (removes 1 penalty)
3. For each nearby mackerel, calculate loss of excluding it (loses 1 count)
4. If excluding a sardine gives net gain, shift the corresponding edge
   - Shift inward by distance sufficient to exclude the sardine
   - Use binary search or incremental adjustment to find optimal shift
5. Track edge changes, apply all that improve score

## Phase 4: Multi-Rectangle Union Handling
- Detect when disjoint clusters produce separate rectangles
- Try merging nearby rectangles if it improves total score
- Ensure merged shape remains simple polygon (no self-intersection)
- Alternative: output union as separate polygon segments if beneficial

## Phase 5: Local Edge Optimization
- For each edge, try shifts: ±5, ±10, ±15, ±20, ±25, ±30 units
- For each shift, compute:
  * New polygon (ensure validity)
  * Count mackerels inside (use point-in-polygon test)
  * Count sardines inside
  * Score = mackerels - sardines + 1
- Keep shift that maximizes score
- Repeat 5-10 iterations, each time starting from refined polygon

## Phase 6: Multiple Restart Strategy
Run 10-15 independent attempts:
- Vary clustering parameters (cell_size: 150, 250, 500)
- Vary which clusters to start with (top K by mackerel count)
- Vary refinement depth (5, 10, 15 iterations)
- Track best polygon across all restarts

## Implementation Notes
- Use KD-tree for O(log N) point queries during optimization
- Pre-read all fish coordinates at start (single pass O(N))
- Point-in-rectangle test: O(1) for initial boxes, O(vertices) for refined
- Time budget: ~1.8s per evaluation, prioritize breadth of exploration
- Output EXACTLY: m (vertices), then m lines of "x y"
- Always validate: non-self-intersecting, perimeter constraint, coordinate bounds
