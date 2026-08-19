---
name: cluster-optimization-playbook
description: Cluster mackerels spatially within 5000-unit radius, build bounding boxes per cluster, audit sardines inside, hill climb edges, and try multi-rectangle unions for separated clusters. Time <1.95s.
---

# Cluster Optimization Playbook

## Overview
Replace grid-based approaches with direct coordinate analysis. The key insight: optimal polygons are unions of axis-aligned rectangles tightly bounding mackerel clusters, not grid-cell expansions.

## Step 1: Parse Coordinates
- Extract all mackerel (type=1) coordinates into a list
- Extract all sardine (type=-1) coordinates into a list
- These are the ground truth; no grid approximation needed

## Step 2: Spatial Clustering
- Set clustering threshold: 5000 units (Euclidean distance)
- For each unassigned mackerel:
  - Find all mackerels within threshold distance
  - Group them into a cluster (BFS/DFS)
  - Record cluster centroid and member count

## Step 3: Bounding Box Construction
For each cluster:
- min_x, max_x = min/max of x-coordinates in cluster
- min_y, max_y = min/max of y-coordinates in cluster
- Rectangle = [min_x, max_x] × [min_y, max_y]
- Perimeter = 2 * (max_x - min_x + max_y - min_y)
- Discard if perimeter > 400,000

## Step 4: Sardine Audit (Critical)
For each rectangle:
- Count sardines where: min_x <= s.x <= max_x AND min_y <= s.y <= max_y
- Points on boundary count as inside (problem statement)
- Score = mackerels_in_cluster - sardines_inside + 1

## Step 5: Edge Hill Climbing
For each rectangle edge:
- Try expanding outward by: +10, +20, +30 units
- Try contracting inward by: -10, -20, -30 units (if perimeter still valid)
- For each variant, recompute sardine count
- Keep changes that increase score
- Repeat 2 refinement rounds

## Step 6: Multi-Rectangle Strategy
- Consider disjoint rectangles as separate entities
- Total score = sum of individual rectangle scores (mackerels - sardines + 1 per rect)
- This captures separated mackerel clusters more effectively than one large union

## Step 7: Output Format
m (vertices)
x0 y0
x1 y1
...
For single rectangle: 4 vertices
For union of rectangles: merge shared edges, output combined vertex list

## Key Differences from Grid Approach
- No grid abstraction: work directly with coordinates
- Precision clustering: 5000-unit threshold, not cell-based
- Exact sardine counting: iterate all sardines, not estimate
- Multi-rectangle support: disjoint rectangles scored independently
- Simpler, more direct optimization path
