---
name: discovery-optimization
description: "Cluster-based minimal bounding box optimization. Detect dense mackerel clusters using spatial grouping, build minimal rectangles around each cluster, optionally merge nearby clusters, try local expansions."
---

# Cluster-Based Polygon Optimization for Fish Capture

## Phase 1: Cluster Detection

Read all mackerel positions from input. Use spatial hashing with 100x100 grid (cell size 1000x1000) to efficiently group nearby mackerels.

Define proximity: two mackerels are in the same cluster if they are within 500 units (Manhattan distance).

Use Union-Find to group mackerels into clusters:
- For each mackerel, check neighbors in the same grid cell and adjacent cells
- Merge clusters when mackerels are close

Count mackerels per cluster and compute cluster center (centroid).

## Phase 2: Minimal Bounding Box Construction

For each cluster:
- Find min_x, max_x, min_y, max_y across all mackerels in the cluster
- Create a rectangle with 4 vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- This rectangle captures all mackerels in the cluster

## Phase 3: Cluster Combination Strategies

Generate multiple candidate polygons:

Strategy A (Single Best):
- Take the cluster with most mackerels
- Use its bounding box

Strategy B (Top 3 Merged):
- Take top 3 clusters by mackerel count
- Compute union bounding box (min of all mins, max of all maxes)

Strategy C (Corridor-Connected):
- Take top 5 clusters
- Sort by x-coordinate
- For adjacent clusters (gap < 300), connect with a thin corridor (1 unit wide)
- Build polygon following cluster boxes connected by corridors

Strategy D (Individual + Local):
- For each cluster, create its bounding box
- Output all bounding boxes (if they don't overlap, they form a multi-polygon; otherwise merge)

## Phase 4: Local Search & Refinement

For each candidate polygon:

1. Edge Expansion:
   - For each edge, try expanding outward by ±5, ±10, ±15 units
   - Check if expansion captures additional mackerels
   - If net gain (mackerels - sardines) > 0, accept

2. Ear Addition:
   - Find individual mackerels not covered by the polygon
   - For nearby uncovered mackerels, try adding a small "ear" (2x2 or 4x4 rectangle)
   - Accept if net gain > 0

3. Corner Smoothing:
   - Try shrinking corners if they only contain sardines (net loss)

## Phase 5: Multiple Restarts

Run 10-15 restarts with different cluster grouping parameters:
- Vary proximity threshold: 400, 500, 600
- Vary number of clusters to consider: 1, 3, 5, 7
- Vary combination strategy

Track the best polygon across all restarts.

## Implementation Notes

- Use O(N log N) or O(N) clustering algorithms
- Bounding box operations are O(1) per cluster
- Polygon validation: ensure axis-aligned, no self-intersection, valid vertex count
- Time budget: ~1.8s for search, leave 0.2s margin
- All coordinates must be integers in [0, 100000]

## Expected Behavior

- Seed program likely makes small/empty polygons
- Our approach should find cluster-based polygons that capture significant mackerel regions
- Local search refines these to avoid sardines
- Multiple restarts ensure we don't miss diverse good solutions
