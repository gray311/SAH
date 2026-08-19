---
name: discovery-optimization
description: "Optimize C++ polygon using coordinate projection and binary search. Find optimal axis-aligned rectangle by projecting fish coordinates, computing 2D prefix sums for O(1) rectangle queries, and systematically searching x-y boundary pairs."
---

# Coordinate Projection + Binary Search Strategy

## Core Insight
The optimal polygon is likely a simple axis-aligned rectangle. We can find it by:
1. Projecting all fish coordinates to x and y axes
2. Using 2D prefix sums for O(1) rectangle score queries
3. Binary searching over boundary pairs to find the optimal rectangle

## Implementation Steps

### Step 1: Build 2D Prefix Sum Grid
- Create a grid covering [0, 100000] x [0, 100000]
- Mark mackerel positions with +1, sardine positions with -1
- Compute 2D prefix sums: grid[i][j] = sum of all points in [0,i] x [0,j]
- Rectangle score = prefix_sum(x_max, y_max) - prefix_sum(x_min-1, y_max) - prefix_sum(x_max, y_min-1) + prefix_sum(x_min-1, y_min-1)

### Step 2: Coordinate Projection
- Collect all unique x-coordinates from mackerels (N points)
- Collect all unique y-coordinates from mackerels (N points)
- Also include unique coordinates from sardines for boundary refinement
- Sort and deduplicate to get candidate boundary arrays X[] and Y[]

### Step 3: Binary Search Over Boundaries
- For each x_min in X[:N/2], x_max in X[N/2:]:
  - Binary search for optimal y_min and y_max that maximize score
  - Use the prefix sum grid for O(1) queries
  - Track best (x_min, x_max, y_min, y_max)

### Step 4: Output Best Rectangle
- Output 4 vertices: (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)
- Ensure perimeter <= 400000 and vertex count <= 1000 (rectangle satisfies this)

## Time Complexity
- Grid construction: O(MAX_COORD^2) = O(10^10) - too slow!
- Instead, use a sparse grid only around mackerel coordinates
- Use coordinate compression: map unique x and y coordinates to [0, N]
- This gives O(N^2) search with O(1) queries, feasible in 2s

## Key Optimization
- Use coordinate compression to reduce 10^5 range to N=5000 points
- Build sparse 2D array of size N x N
- Compute prefix sums in O(N^2)
- Search O(N^2) boundary pairs with O(1) queries
- Total: O(N^2) = O(25*10^6) operations, feasible in 2s
