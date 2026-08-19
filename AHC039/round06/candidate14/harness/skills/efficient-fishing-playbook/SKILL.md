---
name: efficient-fishing-playbook
description: Playbook for Ahc039 - Build KD-tree, compute density grid, find profit regions, construct polygon. Use density-based search instead of random mutations.
---

# Efficient Fishing Playbook

## Goal
Maximize (mackerels - sardines) inside an axis-aligned polygon.

## Step 1: Input Analysis
- Read N, then 2N coordinates.
- First N lines: mackerels (type 1).
- Next N lines: sardines (type -1).

## Step 2: Build Spatial Index
- Construct a KD-tree on all fish positions.
- Use x-axis for first split, y-axis for second, alternating.
- This enables O(log N) rectangle queries.

## Step 3: Density Grid Computation
- Divide the coordinate space into grid cells (e.g., 200x200, each 2000x2000 pixels).
- For each cell [x0,x1]x[y0,y1]:
  - Query KD-tree for fish inside the rectangle.
  - Count mackerels and sardines.
  - Compute net_score = mackerel_count - sardine_count.
- Store results in a 2D grid.

## Step 4: Find Profit Regions
- Identify all cells with net_score > 0.
- Use flood-fill or connected components to group adjacent profitable cells.
- Larger connected components are better candidates.

## Step 5: Polygon Construction
- For each connected profit component:
  - Compute bounding box [x_min, x_max] x [y_min, y_max].
  - Optionally extend to include adjacent profitable cells.
  - Create a polygon from the bounding box vertices.
- Merge overlapping polygons by taking union of regions.

## Step 6: Optimization
- Try multiple constructions: single rectangle, union of rectangles, L-shapes.
- Evaluate each candidate (can use probe_solution for ranking).
- Select the polygon with highest estimated score.

## Step 7: Validation
- Ensure vertex count <= 1000.
- Ensure perimeter <= 400,000.
- Ensure no self-intersections (simple polygon).
- Ensure all vertices are integers in [0, 100000].
- Ensure polygon edges are axis-aligned.

## Step 8: Output
- Print number of vertices.
- Print each vertex (x y) on a separate line.
- Vertices can be in clockwise or counterclockwise order.
