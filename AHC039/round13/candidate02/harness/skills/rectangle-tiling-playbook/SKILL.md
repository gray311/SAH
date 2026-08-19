---
name: rectangle-tiling-playbook
description: Use geometric rectangle tiling to solve fish capture. Build spatial index, score rectangles via inclusion-exclusion, combine into valid polygons, refine iteratively.
---

# Rectangle Tiling for Fish Capture Optimization

## Overview
Instead of grid-based corridor expansion, use axis-aligned rectangles that can be combined into polygons.

## Phase 1: Spatial Index Construction
- Read all fish coordinates (10000 total: 5000 mackerels, 5000 sardines)
- Sort both mackerels and sardines by x-coordinate, then y-coordinate
- Build coarse grid (100x100, cell_size=1000) for O(1) density queries

## Phase 2: Rectangle Scoring
For any rectangle [x1,y1] to [x2,y2]:
- Count mackerels: filter sorted list where x1 ≤ x ≤ x2 and y1 ≤ y ≤ y2
- Count sardines: same
- Score = mackerels - sardines
- Use count_fish_in_rect tool for this query
- Use probe_solution with subsampling for quick estimates

## Phase 3: Candidate Generation
Three complementary strategies:

### Strategy A: Grid-Based Search
- Start from grid cells with highest M-S score
- For each cell, try all rectangles fitting within 1-3 cells
- Score using count_fish_in_rect
- Keep rectangles with positive score

### Strategy B: Cluster Expansion
- Find mackerel clusters (5+ mackerels within 500-unit radius)
- Start rectangle at cluster center, expand in 4 directions
- Expand until: perimeter limit, or sardine count becomes too high (S > M)
- Record rectangle bounds

### Strategy C: Sweep-Line Maxima
- For each x-coordinate that has a mackerel:
  - Find vertical range [y_min, y_max] containing mackerels
  - Slide y-range to maximize M - S
  - If score > 0, consider as candidate
- Deduplicate overlapping candidates

## Phase 4: Polygon Combination
- Combine adjacent rectangles that:
  * Share an edge or overlap
  * Together don't exceed perimeter limit
  * Form a simple polygon (no self-intersection)
- Algorithm:
  1. Sort rectangles by bottom-left coordinate
  2. Merge overlapping rectangles
  3. Combine adjacent into larger shapes
  4. Extract vertices ensuring no self-intersection
  5. Validate perimeter ≤ 400,000

## Phase 5: Iterative Refinement
For each polygon candidate:

### Expansion
- For each edge, try expanding in outward direction by 50, 100, 200 units
- Score new polygon using probe_solution
- Keep expansion if score improves

### Contraction
- If polygon contains high sardine density regions:
  * Split into smaller rectangles
  * Keep only those with positive score
  * Recombine

### Edge Optimization
- For each edge midpoint, try shifting by ±100, ±200, ±300 units
- Keep shift that improves score
- Repeat 2-3 rounds

## Phase 6: Multiple Restarts
Run 10-15 independent searches:
1. Random seed point → grow rectangle
2. Top grid cell → expand to max valid rectangle
3. Best rectangle from A → perturb and improve
4. Multiple small rectangles → merge if beneficial
5. Full-coverage start → iteratively remove low-score regions

## Output
- Single best valid polygon (4-1000 vertices)
- Integer coordinates in [0, 100000]
- Perimeter ≤ 400,000
- Score = max(0, M - S + 1)

## C++ Implementation Tips
- Use std::vector with std::sort for O(N log N) preprocessing
- Rectangle query: simple iteration or use prefix sums on grid
- Grid for O(1) coarse queries, detailed lists for exact counts
- Validate polygon geometry carefully (check self-intersection)
- Time budget: < 2.0s per evaluation
- Always output valid format: m vertices, then m lines of "x y"
