---
name: discovery-optimization
description: "Direct rectangle search with 50x50 grid, prefix-sum O(1) scoring, diverse rectangle generation, limited hill climbing."
---

# Direct Rectangle Search for Polygon Optimization

## Phase 1: Data Loading and Prefix Sum Construction

- Read all 10000 fish coordinates (5000 mackerels, 5000 sardines)
- Build 50x50 grid (cell_size=2000) storing fish coordinates per cell
- Build 2D prefix sum arrays: P_m[x][y] = mackerels in [0,x]x[0,y], similarly for sardines
- O(1) query: sum in rectangle = P[y2][x2] - P[y1][x2] - P[y2][x1] + P[y1][x1]

## Phase 2: Rectangle Candidate Generation

For each grid cell with positive net fish count:

- Generate rectangles centered at cell midpoint
- Size variations: 200x200, 400x400, 600x600, 800x800, 1000x1000
- Position offsets: center ±50, ±100, ±150 in each direction
- Clip all coordinates to [0, 100000]
- Validate: 4 vertices, distinct, perimeter <= 400,000

## Phase 3: Fast Evaluation

- Score each rectangle using prefix sums: O(1) per rectangle
- Track top candidates

## Phase 4: Local Search

For top 5 rectangles:
- For each edge (x1,y1)-(x2,y2), try shifts ±10, ±20
- Recompute score with prefix sums
- Keep shift maximizing mackerels - sardines

## Phase 5: Multiple Restarts

- Run 10 restarts with different seeds
- Each restart: pick 5-8 random dense cells, generate rectangles, hill climb
- Output single best valid rectangle

## Implementation Notes

- Use std::set to verify vertex uniqueness
- Prefix sum arrays sized 100002 x 100002 for full range
- Total time: < 2.0s per evaluation
- Prioritize rectangle diversity over hill climbing depth
