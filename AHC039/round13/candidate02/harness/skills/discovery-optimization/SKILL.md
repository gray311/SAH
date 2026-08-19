---
name: discovery-optimization
description: "Geometric rectangle tiling optimization. Build spatial index, evaluate candidate rectangles using probe, combine into valid polygons, iterate expansion/contraction, run multiple strategies."
---

# Geometric Rectangle Tiling Strategy

## Phase 1: Build Spatial Index
- Read all 10000 fish (5000 mackerels, 5000 sardines) from input
- Store in sorted containers for fast range queries
- Build grid for O(1) cell-level statistics

## Phase 2: Rectangle Scoring (CRITICAL)
For any axis-aligned rectangle [x1,y1] to [x2,y2]:
- Count mackerels: use inclusion-exclusion on sorted lists
- Count sardines: same method
- Score = mackerels - sardines
- Use probe_solution for ~10% subsample to estimate quickly

## Phase 3: Rectangle-Based Search
- Start with grid cells (1000x1000 resolution, giving 100x100 grid)
- For each cell, try all rectangles fitting within 1-3 cells
- Score each using probe (subsample) or evaluate (full)
- Track rectangles with score > 0

## Phase 4: Polygon Construction
- Combine adjacent rectangles into valid polygons
- Use coordinate compression to minimize vertices
- Validate: 4-1000 vertices, perimeter ≤ 400,000, no self-intersection
- Ensure integer coordinates

## Phase 5: Iterative Refinement
- EXPAND: For each polygon edge, try expanding in direction if it improves score
- CONTRACT: For low-scoring regions, shrink polygon
- SPLIT: If polygon has large sardine density, split into smaller polygons
- MERGE: Adjacent high-scoring regions can merge
- Repeat 3-5 rounds per candidate

## Phase 6: Multiple Strategies
Run 10-15 independent searches:
1. Cluster-based: Find mackerel clusters, build rectangles around them
2. Sweep-line: Scan coordinate space, find local maxima
3. Perturb-max: Find best rectangle, perturb and improve
4. Greedy-grow: Start small, greedily add beneficial area
5. Split-merge: Start with full coverage, iteratively split low-scoring regions

Output the single best valid polygon.

## C++ Implementation
- Use std::vector + std::sort for O(N log N) setup
- For rectangle queries: use prefix sums on binned coordinates or binary search
- Grid for O(1) coarse queries
- KD-tree optional for faster queries if needed
- Validate polygon geometry carefully
- Total time per eval: < 2.0s, output valid format
