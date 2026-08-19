---
name: discovery-optimization
description: "Coordinate-space rectangle expansion with 2D prefix sums. Detect mackerel-dense regions, expand rectangles with perimeter awareness, try multi-rectangle combinations, deep local vertex search, 10-12 restarts under 1.8s."
---

# Coordinate-Space Rectangle Optimization

## Core Strategy
Build axis-aligned rectangles directly from fish coordinates using 2D prefix sums for O(1) scoring.

## Phase 1: Preprocessing
- Build 2D prefix sum arrays for mackerels and sardines
- For coordinate (x,y) with cell size 500: prefix_sum[x][y] = count in [0,x]x[0,y]
- Query time: O(1), Build time: O(N + max_coord²/500)

## Phase 2: Dense Region Detection
- Scan x-coordinates in steps of 100 (range 0-100000)
- For each x-range [x, x+100], count total mackerels across all y
- Identify top 10 x-ranges with highest mackerel density
- For each, also compute sardine count for penalty

## Phase 3: Rectangle Expansion
For each dense region at (x0, y0):

### Expansion in 4 directions:
- RIGHT: Increase max_x by 5, 10, 25, 50, 100 units (while perimeter < 400000)
- DOWN: Increase max_y similarly
- LEFT: Decrease min_x (if > 0)
- UP: Decrease min_y (if < 100000)

### At each expansion step:
- Query rectangle score using prefix sums: mackerels - sardines
- Track best score at each perimeter level
- Stop if score becomes negative and stays negative for 3 consecutive sizes

## Phase 4: Multi-Rectangle Combinations
- Try pairing 2 non-overlapping rectangles
- Combined score = sum of individual scores
- Combined perimeter = sum of individual perimeters
- Must satisfy: combined_perimeter <= 400000

## Phase 5: Local Vertex Optimization
For each candidate rectangle (min_x, min_y, max_x, max_y):
- Try perturbing each corner by ±5, ±10, ±25, ±50
- Keep perturbation that maximizes score
- Repeat 2 refinement rounds (each round uses updated corners)

## Phase 6: Multiple Restarts
- Run 10-12 restarts
- Each restart: 
  * Random seed selection of starting x-range
  * Different expansion order (prioritize different directions)
  * Different perturbation randomization
- Track best polygon across all restarts

## Phase 7: Output
- Ensure exactly 4 vertices for rectangles (or 6-12 for multi-rectangle)
- Integer coordinates in [0, 100000]
- Perimeter <= 400000
- Output: m\n x0 y0\n x1 y1\n ...

## C++ Implementation Notes
- Use int arrays for prefix sums (N=5000 fish, max_coord=100000, cell=500 → ~200x200 arrays)
- Rectangle query: sum_rect(x1,y1,x2,y2) = prefix[x2][y2] - prefix[x1][y2] - prefix[x2][y1] + prefix[x1][y1]
- Total time: < 1.8s with efficient prefix sum queries
- No KD-tree needed with O(1) prefix sum scoring
