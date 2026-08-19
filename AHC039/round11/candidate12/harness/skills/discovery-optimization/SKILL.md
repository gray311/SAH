---
name: discovery-optimization
description: "Grid-based axis-aligned polygon optimization. Use prefix sum grid for O(1) rectangle scoring, search for optimal rectangles and their merges, implement iterative improvement with <1.9s runtime."
---

# Grid-Based Axis-Aligned Polygon Optimization

## Phase 1: Grid Setup
- Divide [0, 100000]×[0, 100000] into 500×500 grid (cell_size=200)
- For each cell, count mackerels (M) and sardines (S)
- Build 2D prefix sum arrays: prefix_M[r][c] = sum of M in grid[0:r][0:c]
- Build 2D prefix sum arrays: prefix_S[r][c] = sum of S in grid[0:r][0:c]

## Phase 2: Rectangle Scoring
- Score of rectangle [(x1,y1) to (x2,y2)] = 
  M(x1,y1,x2,y2) - S(x1,y1,x2,y2) + 1
- Use prefix sums: count = prefix[x2][y2] - prefix[x1][y1] - prefix[x2][y1] + prefix[x1][y2]
- Iterate over all possible rectangle positions
- Track best rectangle by score

## Phase 3: Iterative Improvement (Required Search)
- Start with best rectangle found
- For up to 10000 iterations (or until time limit):
  * Try expanding/shrinking each edge by ±20, ±40, ±60
  * Try random rectangle seeds (different corners)
  * Keep improvement if score increases
- Use simulated annealing: accept worse solutions with probability e^(-delta/T)

## Phase 4: Polygon Output
- Convert final rectangle to 4 vertices
- If merged multiple rectangles, ensure valid polygon with ≤1000 vertices
- Verify perimeter ≤ 400000
- Output in required format

## Implementation Notes
- Use int for counts (N=5000 per fish type, max 5000 in any rectangle)
- Use fast I/O (cin.tie(nullptr))
- Precompute all prefix sums in O(GRID_SIZE²)
- Rectangle search is O(GRID_SIZE^4) but with small constant (500 cells each dim)
- Total runtime target: <1.9s for 150 test cases
