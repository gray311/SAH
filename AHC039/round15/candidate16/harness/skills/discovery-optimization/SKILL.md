---
name: discovery-optimization
description: "Coordinate-based rectangle merging. Parse fish coords, build mackerel clusters as bounding boxes, refine edges locally, merge adjacent boxes, 10-15 restarts."
---

# Coordinate-Based Rectangle Optimization

## Phase 1: Coordinate Parsing
- Extract all mackerel (type=1) and sardine (type=-1) coordinates
- Store in sorted vectors for efficient range queries

## Phase 2: Cluster Detection
- For each mackerel, find neighbors within 5000 units
- Group into connected components (clusters)
- For each cluster, compute tight bounding box (min_x, max_x, min_y, max_y)

## Phase 3: Rectangle Refinement
For each cluster bounding box:
- Try 9 coordinate variations per edge:
  * Left edge: min_x - 500, -200, -100, -50, 0, +50, +100, +200, +500
  * Right edge: max_x + 500, +200, +100, +50, 0, -50, -100, -200, -500
  * (Clamp to [0, 100000])
- For each candidate rectangle, count fish using coordinate range queries
- Score = mackerels - sardines + 1

## Phase 4: Combinatorial Merging
- Sort clusters by position
- Try merging adjacent clusters (union of bounding boxes)
- For 2-3 cluster merges, compute resulting polygon (may need convex hull)
- Score each merged shape

## Phase 5: Local Optimization
For promising candidates:
- Try edge shifts: ±50, ±100, ±200, ±500 units per edge
- For rectangles: vary each of 4 edges independently
- For complex shapes: vary each vertex
- Keep best shift if score improves

## Phase 6: Multiple Restarts
- Run 10-15 restarts with different seeds
- Each restart: randomly select 2-3 mackerels as seed points
- Build bounding box around seeds, refine, try 2-3 neighbor merges

## Phase 7: Output
- For rectangles: output 4 vertices
- For merged shapes: output simplified polygon (convex hull or manual simplification)
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
