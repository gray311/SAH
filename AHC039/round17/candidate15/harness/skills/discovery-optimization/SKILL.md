---
name: discovery-optimization
description: "Cluster-based rectangle formation around mackerel groups. Use DBSCAN-like clustering (min_dist=150) to find tight mackerel clusters, build rectangles with small margin, filter by sardine count, merge overlapping rectangles."
---

# Cluster-Based Rectangle Formation

## Phase 1: Spatial Clustering
- Parse mackerel coordinates from input
- Sort by x-coordinate
- Iterate and group: if point x is within 150 of previous group's max x, add to same cluster
- Record cluster bounds (min_x, max_x, min_y, max_y, mackerel_count)

## Phase 2: Rectangle Generation
For each cluster:
- Create rectangle with margin: [min_x-10, max_x+10] x [min_y-10, max_y+10]
- Clip to [0, 100000] bounds
- Count mackerels and sardines inside this rectangle

## Phase 3: Sardine Filtering
- For each rectangle, compute penalty = sardines_inside
- Keep rectangle only if: penalty == 0 OR (mackerels_inside >= 5)
- Track overall mackerels and sardines for kept rectangles

## Phase 4: Merging Overlapping Rectangles
- Find rectangles that overlap or are adjacent
- Merge them into larger rectangles using union algorithm
- Compute new mackerel/sardine counts for merged regions

## Phase 5: Output
- Convert final rectangle(s) to vertex list
- If multiple rectangles: output as multi-vertex polygon (may need to connect them)
- Validate: 4 <= vertices <= 1000, perimeter <= 400000, coords in [0, 100000]
- Output best polygon (highest mackerels - sardines)
