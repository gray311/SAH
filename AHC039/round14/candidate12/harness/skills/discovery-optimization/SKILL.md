---
name: discovery-optimization
description: "Direct geometric construction. Parse fish coordinates, build rectangle candidates from mackerel clusters, hill climb vertices, try 20-30 variants per eval."
---

# Direct Geometric Polygon Construction Strategy

## Phase 1: Input Processing
- Read all fish coordinates into memory (mackerels and sardines separately)
- Build dense representations: for each x coordinate, list of (y, type) pairs
- Compute density maps: for each small region, count mackerels vs sardines

## Phase 2: Multiple Construction Strategies

### Strategy A: Global Bounding Box
- Find min_x, max_x of all mackerels; min_y, max_y of all mackerels
- Build single rectangle [min_x, max_x] x [min_y, max_y]
- Extend outward if improving score (while avoiding sardines)

### Strategy B: Cluster-Based Multi-Rectangle
- Find connected clusters of mackerels (points within distance D=200)
- For each cluster, build minimal bounding rectangle
- Calculate score for each rectangle individually
- Combine rectangles: start with best single, add second best if non-overlapping and improves total

### Strategy C: L-Shaped Polygons
- Pick 2 dense mackerel clusters
- Build rectangles around each, then connect them into L-shape
- Try both orientations

### Strategy D: Randomized Vertex Placement
- Sample random x values from mackerel x-coordinates
- Sample random y values from mackerel y-coordinates
- Form rectangles/polygons from these samples
- Evaluate and keep best

## Phase 3: Hill Climbing
For each candidate polygon:
1. Extract vertices and edges
2. For each vertex, try perturbations: ±5, ±10, ±20, ±50 in x or y direction
3. For each edge, try extending/shrinking by ±5, ±10, ±20
4. Use point-in-rectangle test: for each rectangle in polygon, check if each fish point is inside
5. Score = (#mackerels inside) - (#sardines inside) + 1
6. Keep all perturbations that improve score
7. Repeat 5-10 iterations

## Phase 4: Validation
- Ensure 4 <= vertices <= 1000
- All coordinates in [0, 100000]
- Perimeter <= 400,000
- No self-intersection (axis-aligned rectangles don't self-intersect if non-overlapping)
- Output format: vertex count, then vertex coordinates

## C++ Implementation Notes
- Use direct coordinate arrays, no grid
- Implement point-in-rectangle test efficiently
- For multi-rectangle polygons, track which rectangles form the shape
- Use std::vector for dynamic arrays
- Implement multiple construction strategies and try all, keep best
- Total time: < 2.0 seconds per evaluation
