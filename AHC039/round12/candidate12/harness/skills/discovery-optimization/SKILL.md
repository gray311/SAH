---
name: discovery-optimization
description: "Grid-based local search: build 200x200 grid, start minimal polygon on best cell, iteratively expand/shrink/rotate corners using grid queries for fast scoring, 500+ iterations, occasional restarts."
---

# Grid-Based Local Search Strategy

## Phase 1: Grid Construction
- Divide 0-100000 range into 200x200 grid (500 units per cell)
- Count mackerels (type=1) and sardines (type=-1) in each cell
- Precompute prefix sums for O(1) rectangle queries
- cell_score[r][c] = mackerels - sardines in that cell

## Phase 2: Initialization
- Find the cell with maximum positive score (M - S > 0)
- Create minimal polygon: a rectangle around that cell's boundaries
- Rectangle: [cell_x, cell_x+500] x [cell_y, cell_y+500]
- Verify: perimeter <= 400000, all coords valid

## Phase 3: Local Search Loop
Iterate up to 500 times or until timeout (~1.5s):

### Move Types (try all, keep best):
1. **Expand Edge**: For each of 4 edges, extend outward by 1-20 units
   - Query new rectangle area with grid
   - Check score improvement

2. **Shrink Edge**: Contract each edge inward by 1-10 units
   - Useful for removing sardine-rich borders

3. **Corner Rotation**: 90-degree pivot of corners
   - Change corner from (x,y) to adjacent grid point in another direction

4. **Vertex Flip**: Replace each vertex with the grid center point that maximizes score
   - Smart local optimization

### Scoring:
- Use grid-based rectangle sum: for polygon, decompose into grid-aligned rectangles
- Sum M - S for all rectangles, add 1

### Restarts:
- Every 100 iterations, do a random restart:
  - Pick 2-4 random cells
  - Build small polygons around them
  - Merge if beneficial

## Phase 4: Output
- Ensure exactly 4-1000 vertices
- Output in format: m\n x1 y1\n x2 y2\n ...
- Always valid axis-aligned polygon
