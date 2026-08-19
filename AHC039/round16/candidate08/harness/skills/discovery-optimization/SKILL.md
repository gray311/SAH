---
name: discovery-optimization
description: "Rectangle covering with coordinate partitioning. Build prefix sum grid from fish coordinates, find high (M-S) rectangles, refine boundaries by 1-10 units, 5-8 restarts."
---

# Rectangle Covering Strategy for Axis-Aligned Polygon Optimization

## Phase 1: Coordinate Partitioning

- Collect all unique x coordinates from mackerels and sardines: x_0, x_1, ..., x_{2N-1}
- Collect all unique y coordinates: y_0, y_1, ..., y_{2N-1}
- Sort and deduplicate: X[0] < X[1] < ... < X[u] and Y[0] < Y[1] < ... < Y[v]
- This creates (u) vertical strips and (v) horizontal strips

## Phase 2: Prefix Sum Grid Construction

- Create a grid indexed by coordinate positions
- For each fish at (fx, fy), find its grid position and increment count
- Build 2D prefix sum array P[i][j] = sum of fish in rectangle [0,i]x[0,j]
- Fish count in rectangle [x1,x2]x[y1,y2] = query in O(1) using prefix sums

## Phase 3: Rectangle Search

- Iterate over all pairs of X boundaries (Xi, Xj) where i < j
- Iterate over all pairs of Y boundaries (Yk, Yl) where k < l
- Score = query(xi, xj, yk, yl) for mackerels minus sardines + 1
- Track best rectangle found

## Phase 4: Boundary Refinement

- For the best rectangle [x_min, x_max] x [y_min, y_max]:
  - Try x_min-1, x_min-2, ..., x_min-5 (move left)
  - Try x_max+1, x_max+2, ..., x_max+5 (move right)
  - Try y_min-1, y_min-2, ..., y_min-5 (move down)
  - Try y_max+1, y_max+2, ..., y_max+5 (move up)
  - Keep shifts that improve score while staying in [0, 100000]
  - Repeat refinement 2-3 times

## Phase 5: Multiple Restarts

- Run 5-8 restarts with different seed perturbations
- Each restart uses same coordinate partitioning but different refinement paths
- Output best rectangle across all restarts

## Output Format

- m = 4
- x_min y_min
- x_max y_min
- x_max y_max
- x_min y_max
