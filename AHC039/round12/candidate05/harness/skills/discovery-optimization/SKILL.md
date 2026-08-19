---
name: discovery-optimization
description: "Coordinate-based geometric search. Cluster fish by x,y, build rectangles/L/U shapes, validate, score, refine, 10 restarts."
---

# Coordinate-Based Geometric Search

## Overview

Instead of grid corridors, directly cluster fish coordinates and build simple valid polygons.

## Phase 1: Input Parsing

- Read N mackerels: (x_0, y_0) to (x_{N-1}, y_{N-1})
- Read N sardines: (x_N, y_N) to (x_{2N-1}, y_{2N-1})
- Store in separate vectors

## Phase 2: Clustering

- Sort mackerels by x, then by y
- Sort mackerels by y, then by x
- Identify clusters: points within 100 units in either dimension
- Track cluster centers and bounding boxes

## Phase 3: Polygon Generation

### Rectangle (simplest, most likely to be valid):
- For each cluster, create rect: [min_x, min_y, max_x, max_y]
- 4 vertices, guaranteed valid if coords in bounds

### L-Shape:
- Pick two clusters C1, C2
- Create rect1 from C1, rect2 from C2
- Join at corner: find overlapping region, create 6-vertex polygon

### U-Shape:
- Pick three clusters C1, C2, C3
- Form U with open side in one direction
- 8-10 vertices

## Phase 4: Validation

For each candidate polygon:
1. Check vertex count: 4 <= n <= 1000
2. Check perimeter: sum of edge lengths <= 400,000
3. Check bounds: all (x,y) in [0, 100000]
4. Check axis-aligned: each edge is horizontal or vertical
5. Check closed: vertices[0] != vertices[-1] (but edge exists)
6. Check no self-intersection: for each non-adjacent edge pair, check intersection

## Phase 5: Scoring

For each valid polygon:
- Use point-in-polygon test for each fish
- Points on edges count as inside
- m_count = count mackerels inside
- s_count = count sardines inside
- score = max(0, m_count - s_count + 1)

## Phase 6: Refinement

For each top 5-10 candidates:
- For each edge, try shifts: ±5, ±10, ±15 units
- Re-validate shifted polygon
- Re-score if valid
- Keep best

## Phase 7: Restarts

Run 10 restarts:
- Each with different random seed for clustering perturbation
- Different polygon type priority per restart
- Track best polygon across all restarts

## Time Budget

- < 2.0 seconds per evaluation
- Aim for: 100+ candidates, all validated, top 10 refined
- Use efficient O(n log n) clustering (sort + scan)
- Use efficient O(n^2) polygon validation (only for ~100 candidates with 1000 max vertices)
- Use O(N*n) scoring (N=5000, n=1000 worst case = 5M ops, OK)
