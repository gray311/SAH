---
name: spatial-grid-optimization-guide
description: Use 2D spatial grid indexing to enable O(vertices) polygon scoring. Build grid once, then score many polygon variants quickly.
---

# Spatial Grid-Based Polygon Optimization Guide

## Core Idea

Instead of O(N) point-in-polygon checks, use a 2D grid hash table to score polygons in O(vertices) time.
This enables exploring 10-100x more polygon variants within the time budget.

## Phase 1: Build Spatial Grid

- Create a grid (e.g., 100×100, cell_size=1000) covering [0,100000]×[0,100000]
- For each mackerel and sardine, increment counts in the corresponding cell
- Precompute prefix sums or use simple cell counting for O(1) cell queries

## Phase 2: Fast Polygon Scoring

For any axis-aligned polygon:

1. Decompose the polygon into O(vertices) elementary rectangles
2. For each rectangle, identify which grid cells it covers
3. Sum the fish counts from those cells
4. Compute score = mackerels - sardines + 1

Time complexity: O(vertices × number_of_cells_covered) which is typically much less than O(N).

## Phase 3: Efficient Hill Climbing

- For each edge, try small shifts (±1, ±2, ±5)
- Use the grid to compute the delta in score without full recomputation
- Keep shifts that improve the score
- Repeat until no improvement

## Phase 4: Multiple Search Strategies

### Strategy A: Rectangle with Lobes
- Start with bounding rectangle of mackerels
- Add rectangular lobes in cardinal directions
- Use grid to quickly evaluate each lobe addition

### Strategy B: Morphological Operations
- Start with seed polygon
- Apply dilation/erosion
- Use grid for fast evaluation

### Strategy C: Grid-Based Search
- Sample points in mackerel-dense regions
- Build polygon around clusters
- Use grid to verify coverage

## Key Success Factors

- Build grid ONCE at program startup
- Score many polygon candidates with the grid
- Only call full evaluate_solution on promising candidates
- Use probe_solution for rapid ranking
- Ensure <2.0s total execution time

## Implementation Hints

- Use std::vector<std::pair<int,int>> for grid cells
- Use std::map or coordinate compression for sparse grids
- For 100×100 grid, flat array of 10000 cells is fastest
- Use bit manipulation or simple division for cell indexing
