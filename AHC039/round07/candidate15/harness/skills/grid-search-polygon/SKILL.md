---
name: grid-search-polygon
description: Use grid-based indexing and diverse polygon shapes to maximize fish capture score.
---

# Grid-Based Polygon Search for Fish Capture

## Overview
We have 5000 mackerels and 5000 sardines on a 100000x100000 plane.
Build a 100x100 grid where each cell is 1000x1000 units.
Each cell stores (mackerel_count, sardine_count).

## Grid Index Construction
1. Initialize 100x100 grid with zeros
2. For each fish at (x, y):
     - cell_x = min(x // 1000, 99)
     - cell_y = min(y // 1000, 99)
     - grid[cell_x][cell_y].mackerels += (fish.type == 1)
     - grid[cell_x][cell_y].sardines += (fish.type == -1)

## Grid Query (O(number of cells crossed))
To count fish in rectangle [minX, maxX] x [minY, maxY]:
- cell_min_x = minX // 1000, cell_max_x = maxX // 1000
- cell_min_y = minY // 1000, cell_max_y = maxY // 1000
- Sum grid cells from (cell_min_x, cell_min_y) to (cell_max_x, cell_max_y)

## Polygon Constructors
1. **simple_rect()**: Axis-aligned rectangle. Pick 4 corners from grid cells with many mackerels and few sardines.

2. **l_shape_top_right(minX, maxX, minY, maxY, indentX, indentY)**: 
   - Rectangle [minX, maxX] x [minY, maxY] minus bottom-left corner
   - Helps avoid sardine clusters in one corner while keeping mackerels
   - 6 vertices

3. **stepped_enclose()**: Create staircase pattern around dense mackerel regions
   - Start at left edge, alternate right/up moves
   - Can tightly enclose mackerel clusters while excluding sardines

## Iterative Refinement
For each vertex (x, y), try moves:
- x' = x + delta where delta in [-10, -5, -1, 0, 1, 5, 10]
- y' = y + delta where delta in [-10, -5, -1, 0, 1, 5, 10]
- Keep move only if score increases AND perimeter doesn't exceed 400000
- Try 50 refinements per polygon

## Sardine Avoidance Strategy
- Before finalizing polygon, check if any sardines are near edges
- If sardine at (sx, sy) is within 50 units of edge, indent edge by 10-20 units away
- This may lose some mackerels but saves many sardines

## Time Budget Allocation (2.0s total)
- Grid build: 0.05s
- Generate 20 seed polygons: 0.3s
- Refine top 10: 0.7s
- Try 5 L-shapes + 5 stepped: 0.4s
- Final polish: 0.35s
- Safety margin: 0.2s (stop at 1.8s)
