---
name: discovery-optimization
description: "Rectangle sweep optimization with 2D prefix sums. Parse fish, build grid, compute prefix sums, search all rectangle boundaries for max M-S score, validate perimeter constraints."
---

## Rectangle Sweep Optimization

### Phase 1: Data Parsing
- Read N=5000 mackerels and N=5000 sardines
- Store all fish with type (+1 for mackerel, -1 for sardine)

### Phase 2: Grid Construction
- Create 1000x1000 grid (cell_size=100, covering 0-100000)
- For each fish, increment grid[y//100][x//100] by fish type

### Phase 3: Prefix Sum Computation
- Compute 2D prefix sums in O(grid_rows * grid_cols)
- prefix[i][j] = sum of grid[0..i][0..j]
- Query rectangle score in O(1): prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]

### Phase 4: Rectangle Search
- Iterate all possible top-left (x1,y1) and bottom-right (x2,y2) coordinates
- Use prefix sums for instant M-S score
- Track best rectangles meeting constraints: perimeter <= 400,000, vertices <= 1000
- Consider both single rectangles and combinations (e.g., two non-overlapping rectangles)

### Phase 5: Output
- Output best valid polygon
- If multiple solutions exist, output the last one evaluated
