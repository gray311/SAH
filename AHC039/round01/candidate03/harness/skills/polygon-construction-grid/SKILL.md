---
name: polygon-construction-grid
description: Use grid-based spatial partitioning to construct optimal polygons for the fish trap problem. Identify high-ratio cells and merge them into minimal axis-aligned polygons.
---

# Grid-Based Polygon Construction Playbook

## Overview
Partition the 2D plane into a grid, compute mackerel/sardine ratios per cell,
select high-ratio cells, and construct a minimal polygon covering them.

## Step 1: Choose Grid Size
- Start with G=100 (100×100 = 10,000 cells for 0-100000 range).
- Adjust based on fish density: fewer cells if fish clustered, more if uniform.
- Too coarse: miss local high-ratio areas. Too fine: more cells to process.

## Step 2: Compute Cell Statistics
For each cell:
- Count mackerels (type=1) and sardines (type=-1).
- Ratio = mackerels / (sardines + 1).
- Score = mackerels - sardines + 1 (the objective).

## Step 3: Select High-Ratio Cells
Options:
- Top-K cells by ratio (e.g., K=500).
- Cells with ratio > threshold (e.g., >1.5).
- Combination: top-K with ratio > threshold.

## Step 4: Merge Adjacent Cells
- Use union-find or BFS to merge adjacent high-ratio cells.
- For each merged group, compute the bounding box.
- Bounding box of cells with grid positions [r1,c1] to [r2,c2]:
  x_min = c1 * cell_size, x_max = (c2+1) * cell_size
  y_min = r1 * cell_size, y_max = (r2+1) * cell_size

## Step 5: Construct Polygon
- For each bounding box (rectangle), get 4 vertices.
- Connect rectangles in sorted order (e.g., by centroid, then by x).
- Merge collinear vertices.
- Ensure no self-intersection (axis-aligned polygons are simpler).

## Step 6: Validate
- Vertex count ≤ 1000.
- Perimeter ≤ 400,000.
- All coordinates 0-100,000.
- No self-intersection.

## Step 7: Internal Search Loop
Before final submission, try parameter variations:
- Grid sizes: 50, 100, 200.
- K values: 500, 800, 1000, 1500.
- Thresholds: 1.0, 1.5, 2.0.
- Selection methods: top-K, ratio > threshold, top-K + ratio > threshold.
- Keep the best score.

## Implementation Notes
- Use a flat 2D array for grid cells.
- Pre-sort fish by coordinates for O(1) cell assignment.
- Use union-find for efficient cell merging.
- Finish internal search by T - 0.1s.
