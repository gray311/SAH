---
name: discovery-optimization
description: "Rectangle enumeration via coordinate geometry. Extract unique x/y coordinates from fish, enumerate candidate rectangles, use 2D prefix sums for O(1) counting, enforce perimeter constraint, output valid 4-vertex axis-aligned polygon."
---

# Rectangle Optimization via Coordinate Geometry

## Core Insight

Instead of building corridors or using grids, enumerate optimal axis-aligned rectangles directly using coordinate geometry.

## Step 1: Coordinate Extraction
- Read all fish positions (mackerels and sardines)
- Extract unique x-coordinates: X = sorted(set(all_x))
- Extract unique y-coordinates: Y = sorted(set(all_y))
- These define candidate rectangle boundaries

## Step 2: Efficient Counting with 2D Prefix Sums
- Create a grid/grid-size based on unique coordinates or fixed resolution
- Build 2D prefix sum array: prefix[i][j] = count of fish in rectangle [0,0] to [X[i], Y[j]]
- Count fish in any rectangle in O(1): count(x1,y1,x2,y2) = prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]

## Step 3: Rectangle Enumeration Strategies

### Strategy A: Coordinate-Aligned Rectangles
For each pair of unique x-coordinates (xi, xj) where xi < xj:
  For each pair of unique y-coordinates (yk, yl) where yk < yl:
    - Calculate perimeter: 2 * ((xj-xi) + (yl-yk))
    - If perimeter > 400000, skip
    - Count mackerels and sardines using prefix sums
    - Track max score

### Strategy B: Layered/Sweep Optimization
For efficiency, try:
  - For each y1, sweep y2 from y1+1 upward, stop when perimeter constraint violated
  - For each x1, sweep x2 from x1+1 upward, stop when perimeter constraint violated
  - Use nested loops with early termination

### Strategy C: Dense Region Focus
- Identify regions with high mackerel density
- Focus enumeration on rectangles covering these regions
- Use heuristic pruning based on local density

## Step 4: Perimeter and Constraint Checking
- For rectangle (x1,y1) to (x2,y2): perimeter = 2*(x2-x1 + y2-y1)
- Must satisfy: perimeter <= 400000
- All coordinates must be integers in [0, 100000]
- Rectangle must have at least 4 vertices

## Step 5: Final Output
- Output the rectangle with maximum (mackerels - sardines)
- Format: 4 (num_vertices), then 4 lines of x y coordinates
- Ensure no self-intersection (rectangle is always valid if axis-aligned)

## C++ Implementation Notes
- Use std::unordered_set or std::set for unique coordinates
- Build 2D prefix sum array efficiently (O(N log N) for grid)
- Enumerate rectangles with early termination for perimeter constraint
- Track best rectangle and update on improvement
- Total time: < 2.0s per evaluation with optimized counting
