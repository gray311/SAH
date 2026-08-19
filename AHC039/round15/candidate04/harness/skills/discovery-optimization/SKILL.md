---
name: discovery-optimization
description: "Grid-based density peak finding with compact rectangle construction. Build 100x100 grid, compute M-S counts, use 2D prefix sums for O(1) rectangle queries, find local peaks, expand into compact rectangles, run 10-15 restarts."
---

# Grid-Based Density Peak Optimization Strategy

## Core Idea

Instead of linear corridors, build compact rectangles around local mackerel density peaks.
Use 2D prefix sums for O(1) rectangle scoring to quickly evaluate many candidates.

## Step-by-Step Method

### Step 1: Grid Construction

- Divide [0,100000]x[0,100000] into 100x100 grid (cell_size=1000)
- For each cell, count mackerels and sardines from input points
- Build 2D prefix sum arrays for both M and S counts

### Step 2: Density Peak Identification

- Compute score = M - S for each cell
- Find top 10 cells with highest positive score
- Also consider cells near boundaries

### Step 3: Rectangle Expansion

For each peak cell, expand outward to form rectangles:
- Start with the cell as a 1x1 rectangle
- Try expanding each dimension by increasing amount (1, 2, 3, ... cells)
- Use prefix sums to compute M-S in O(1)
- Stop when M-S decreases or perimeter budget exceeded
- Keep all candidate rectangles with M-S > 0

### Step 4: Multi-Peak Combination (Optional)

- Check if adjacent rectangles can be merged
- Prefer keeping separate compact rectangles if combined shape is less compact

### Step 5: Hill Climbing

- For top candidate rectangles, try slight adjustments:
  - Shift one boundary by ±100, ±200, ±300 units
  - Re-evaluate using prefix sums
  - Keep best adjustment

### Step 6: Randomized Restarts

- Run 10-15 restarts with different seeds
- Each restart: pick random starting cell, build local grid, find peak, construct polygon
- Output best polygon across all restarts

## C++ Implementation Notes

- Use 100x100 fixed grid arrays
- Precompute prefix sums at startup: O(grid_size^2)
- Rectangle query is O(1): sum = P[max_r][max_c] - P[min_r-1][max_c] - P[max_r][min_c-1] + P[min_r-1][min_c-1]
- Total time per evaluation: < 2.0s
- Output format: m (vertices count), then m lines of "x y" coordinates
