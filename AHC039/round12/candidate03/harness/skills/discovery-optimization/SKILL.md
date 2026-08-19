---
name: discovery-optimization
description: "Simple grid-based rectangle optimization. Build 200x200 grid with prefix sums, enumerate rectangles anchored at high M-S cells, filter by constraints, tune edges, run 10-15 restarts. Focus on correctness for all 150 test cases."
---

# Grid-Based Rectangle Optimization Strategy

## Phase 1: Grid Construction
- Create 200x200 grid with cell_size=500 (covers [0,100000]x[0,100000])
- For each fish, increment appropriate cell counts (M for mackerel, S for sardine)
- Compute 2D prefix sums for O(1) rectangle queries

## Phase 2: Rectangle Scoring
- Rectangle score = prefix_sum(max_x, max_y) - prefix_sum(min_x-1, max_y) - prefix_sum(max_x, min_y-1) + prefix_sum(min_x-1, min_y-1)
- M-S score = mackerel_count - sardine_count + 1

## Phase 3: Rectangle Enumeration
- Find cells with highest M-S ratio
- For each such cell, try rectangles extending in various directions
- Track valid rectangles (perimeter <= 400,000, vertices <= 1000, coords in range)

## Phase 4: Edge Tuning
- For top candidates, try small adjustments to corner coordinates (±5, ±10)
- Re-compute score using prefix sums
- Keep best adjustments

## Phase 5: Multiple Restarts
- Run 10-15 restarts with different seeds
- Each restart: perturb starting cell, enumerate rectangles, tune
- Output best rectangle across all restarts

## Implementation Notes
- Use efficient prefix sum computation
- Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y) - 4 vertices
- Always validate output before evaluation
- Time budget: <2.0s per evaluation
