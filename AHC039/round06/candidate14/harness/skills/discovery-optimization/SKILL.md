---
name: discovery-optimization
description: "Solve the \"Efficient Fishing\" task by constructing an axis-aligned polygon that maximizes (mackerels - sardines) inside it. Use KD-tree for spatial queries and density-based region selection."
---

# Ahc039: Efficient Fishing Solver

## Overview
You have N mackerels (type 1) and N sardines (type -1). Build an axis-aligned polygon maximizing (mackerels_inside - sardines_inside).

## Step-by-step algorithm
1. PARSE INPUT: Read N, then 2N lines of (x,y). First N are mackerels, next N are sardines.
2. BUILD KD-TREE: Create a KD-tree of ALL fish positions for O(log N) rectangular queries.
3. DENSITY GRID: Create a 2D grid (e.g., 200x200 or 50x50 cells). For each cell, query the KD-tree for fish inside, compute net = mackerel_count - sardine_count.
4. FIND PROFIT REGIONS: Identify grid cells with positive net score. Group adjacent profitable cells into connected components.
5. CONSTRUCT POLYGON: For each connected profit component, construct a minimal bounding polygon (rectangle or union of rectangles). Merge overlapping polygons.
6. OPTIMIZE SHAPE: Try variations: expand to nearby profitable cells, try different rectangle unions, ensure no self-intersection.
7. VALIDATE CONSTRAINTS: Vertex count <= 1000, perimeter <= 400000, integer coordinates in [0,100000], no self-intersection.
8. OUTPUT: Print vertex count, then each vertex (x y).

## KD-tree usage
- Build tree on x-coordinate, alternate to y for balancing.
- Query rectangle [min_x, max_x] x [min_y, max_y] in O(log N + k) where k = fish inside.
- Use for rapid density computation.

## Polygon construction tips
- Start with the largest connected profit component.
- For a component, compute bounding box [x_min, x_max] x [y_min, y_max].
- Optionally extend to adjacent profitable cells.
- Ensure vertices are distinct and polygon is simple.
- Edge length sum must not exceed 400000.

## Time management
- You have ~1.9s before timeout.
- Build KD-tree once (~0.2s).
- Grid density computation (~0.3s for 200x200 grid).
- Polygon construction and validation (~0.4s).
- Leave ~0.9s for optimization/search variations.

## Common pitfalls
- Self-intersecting polygon: ensure vertices form a simple cycle.
- Perimeter too large: use minimal bounding boxes.
- Missing profitable cells: scan all grid cells, not just those with fish.
- Coordinate range: all vertices must be in [0, 100000].
- Vertex count: keep polygon simple, merge collinear vertices.
