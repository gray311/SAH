---
name: rectangle-from-density
description: Build axis-aligned rectangles from mackerel-dense regions using 2D histogram analysis. Find connected positive-density cells, compute bounding boxes, output best rectangles.
---

# Rectangle-from-Density Strategy

## Overview
Parse fish positions, build a 2D histogram, find connected regions of mackerel-dense cells,
and construct axis-aligned rectangles around each region.

## Step-by-Step Algorithm

### 1. Build Histogram Grid
- Divide [0, 100000]x[0, 100000] into a regular grid (e.g., 200x200, 1000x1000 cells)
- Cell size: 500 units per cell for 200x200 grid
- For each fish, increment the count in its cell (mackerels in M bucket, sardines in S bucket)
- Compute cell score = M - S

### 2. Find Positive-Density Regions
- A positive-density region has M >= S (score >= 0)
- Use connected components (flood-fill / BFS / DFS) with 4-connectivity
- Each component is a cluster of adjacent positive cells

### 3. Compute Bounding Boxes
- For each connected component:
  - Find min_x, max_x, min_y, max_y across all cells
  - Create rectangle: (min_x, min_y) to (max_x, max_y)
  - Convert cell coordinates to pixel coordinates
- Each bounding box has exactly 4 vertices

### 4. Evaluate Each Rectangle
- For each bounding box, do exact fish counting:
  - Count mackerels strictly inside the rectangle
  - Count sardines strictly inside the rectangle
  - Note: points on edges count as inside
- Score = M_inside - S_inside + 1

### 5. Output Best Rectangle
- Track rectangle with maximum score
- Output as polygon with 4 vertices in order
- If no positive region, output minimal rectangle at origin

## Implementation Tips

- Use integer arithmetic only (no floating point)
- Precompute cell-to-pixel mappings
- For exact counting, use O(N) iteration over fish list (fast enough)
- 200x200 grid with 10000 fish is very fast to build
- Edge case: single fish = positive region
- Edge case: all cells negative = use fallback rectangle
