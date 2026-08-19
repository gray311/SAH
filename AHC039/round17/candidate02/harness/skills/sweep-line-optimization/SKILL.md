---
name: sweep-line-optimization
description: Use 2D prefix sums for O(1) rectangle scoring. Parse fish, build grid, compute prefix sums, sweep over all boundaries to find max M-S rectangle.
---

## Sweep-Line Rectangle Optimization

### Core Idea
Use 2D prefix sums to compute any rectangle's mackerel-sardine score in O(1) time,
enabling exhaustive search over all possible rectangle boundaries within the time limit.

### Step 1: Parse Fish Positions
- Read all N mackerels (type +1) and N sardines (type -1) from input
- Store as list of (x, y, type) tuples

### Step 2: Build Grid
- Create 1000x1000 grid (cell_size=100) covering [0, 100000]x[0, 100000]
- For each fish at (x, y), increment grid[y//100][x//100] by type

### Step 3: Compute Prefix Sums
- Build 2D prefix sum array: prefix[i][j] = sum of grid[0..i-1][0..j-1]
- Compute in O(rows*cols) time

### Step 4: Query Rectangle Scores in O(1)
- Score of rectangle [(x1,y1), (x2,y2)] = prefix[y2][x2] - prefix[y1][x1] - prefix[y2][x1-1] + prefix[y1][x1-1]

### Step 5: Exhaustive Boundary Search
- Iterate all possible top-left (x1, y1) and bottom-right (x2, y2) coordinates
- Use prefix sums for instant scoring
- Track rectangles with score > 0 and perimeter <= 400,000

### Step 6: Output Best Rectangle
- Ensure vertices <= 1000, coords in [0,100000]
- If no positive score found, output minimal valid polygon (score = 1)
