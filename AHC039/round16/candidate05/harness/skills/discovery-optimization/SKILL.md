---
name: discovery-optimization
description: "Cluster-focused polygon construction. Detect mackerel-dense cells, build minimal enclosing rectangles with sardine avoidance (S>5 or density<0.3), merge nearby clusters, minimal refinement with \u00b110..30 shifts, 8-10 restarts."
---

# Cluster-Focused Polygon Strategy

## Phase 1: Spatial Analysis
- Parse input to extract all fish coordinates (first N mackerels, next N sardines)
- Build 200x200 grid (cell_size=500) over [0,100000]x[0,100000]
- For each cell, count mackerels (M) and sardines (S)
- Compute density_ratio = M / (M+S) if M+S > 0, else 0

## Phase 2: Cluster Detection
- Sort cells by M count descending
- Select top 20 cells with M >= 5 as "cluster centers"
- Mark avoidance cells: S > 5 OR density_ratio < 0.3

## Phase 3: Minimal Rectangle Construction
For each cluster center cell (r,c):
  - Define initial rectangle: [c, c+1] × [r, r+1] (covers the cell)
  - Expand East: increment column while cell has M > 0 and no avoidance
  - Expand West: decrement column while cell has M > 0 and no avoidance
  - Expand South: increment row while cell has M > 0 and no avoidance  
  - Expand North: decrement row while cell has M > 0 and no avoidance
  - Cap expansion at 100 cells in each direction
  - Store resulting rectangle [min_x, max_x] × [min_y, max_y]

## Phase 4: Cluster Merging
- For each pair of rectangles, if distance < 150 cells, merge:
  - New rectangle: [min(x1,x2), max(x1,x2)+1] × [min(y1,y2), max(y1,y2)+1]
- Remove duplicates (same rectangle from multiple centers)
- Convert to polygon vertices (4 corners for each merged rectangle)

## Phase 5: Minimal Refinement
For each polygon edge:
  - Try shifts: ±10, ±20, ±30 units (only in axis-aligned directions)
  - For each shift, estimate score change using grid sums
  - Accept shift only if it increases (M-S) in affected region
  - Max 2 refinement rounds per polygon

## Phase 6: Strategic Restarts
- Run 8-10 restarts with different random seeds
- Each restart: randomly select 5-8 cluster centers from top 20
- Build minimal rectangles, merge nearby ones, apply refinement
- Track best polygon across all restarts

## Phase 7: Validation and Output
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
- All vertices distinct, axis-aligned edges only
- Output: m followed by m vertex pairs

## C++ Implementation Notes
- Use fixed 200x200 grid for O(1) cell access
- Rectangle query = sum of grid cells in rectangular range
- Total time < 2.0s with efficient operations
- Use std::random_device for restart seeds
