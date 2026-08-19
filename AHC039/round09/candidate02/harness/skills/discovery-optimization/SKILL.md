---
name: discovery-optimization
description: "Direct rectangle search with O(1) grid counting. Find mackerel cluster boundaries, generate rectangle candidates, score with prefix sum grid, keep best within perimeter constraint."
---

# Direct Rectangle Search Strategy

## Core Idea
Instead of building corridors, directly search for optimal axis-aligned rectangles using grid-based O(1) counting.

## Phase 1: Grid Construction
- Build 100001x100001 prefix sum grids for mackerels and sardines
- grid_m[x][y] = count of mackerels in rectangle [0,x]x[0,y]
- grid_s[x][y] = count of sardines in rectangle [0,x]x[0,y]

## Phase 2: Candidate Generation
- Extract unique x and y coordinates from mackerel positions
- Limit to top 200 x-coordinates and 200 y-coordinates (most mackerel-rich)
- Generate all rectangle combinations from these coordinates
- Filter by perimeter <= 400,000 and valid coordinates

## Phase 3: Scoring
- For each rectangle, compute: score = (mackerels - sardines + 1)
- Use prefix sum formula: rect_count = prefix_max - prefix_minx - prefix_maxy - prefix_minxy + prefix_min
- Keep top candidates

## Phase 4: Local Optimization
- For best rectangle, try boundary adjustments ±1, ±5, ±10
- Verify constraints after each adjustment
- Keep improvements

## Phase 5: Output
- Output 4 vertices of best rectangle
- Ensure clockwise or counter-clockwise order

## Time Complexity
- Grid construction: O(N) where N = number of fish
- Rectangle scoring: O(1) per rectangle
- Search: O(X*Y) where X,Y = number of unique coordinates (~40000 pairs max, but filtered to ~40000)
- Total per eval: < 2.0s
