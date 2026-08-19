---
name: discovery-optimization
description: "Spatial clustering with probe-guided expansion. Use find_fish_clusters to locate dense mackerel regions, build axis-aligned rectangles, expand using probe_solution for fast ranking, 10-15 restarts, deep hill climbing with \u00b110..50 shifts."
---

# Spatial Clustering with Probe-Guided Expansion

## Overview
Maximize mackerels - sardines by building axis-aligned polygons around dense mackerel clusters while avoiding sardines.

## Phase 1: Cluster Analysis (ONCE)
- Call find_fish_clusters to build a quadtree of all 10,000 fish points
- Returns: list of mackerel-rich regions (count, center_x, center_y, coverage_area)

## Phase 2: Base Rectangle Construction
For each mackerel cluster from Phase 1:
- Create initial rectangle: [min_x, max_x] × [min_y, max_y] from cluster points
- Ensure at least 4 vertices forming a valid axis-aligned rectangle

## Phase 3: Corridor Expansion
For each base rectangle:
- Expand in 4 directions (N,S,E,W) step by step
- At each step, use probe_solution to check if expansion improves score

## Phase 4: Deep Hill Climbing
For each candidate polygon (up to 1000 vertices):
- For each edge: try shifts ±10, ±20, ±30, ±40, ±50 units in both directions
- Use probe_solution to evaluate shifted polygon (1 probe per shift attempt)

## Phase 5: Multiple Restarts
- Run 10-15 restarts with different cluster selections
- Track best polygon across all restarts

## Phase 6: Final Validation
- Output exactly: m (vertex count 4-1000)
- Then m lines of "x y" (integer coordinates in [0,100000])

## C++ Implementation Notes
- Use std::set or KD-tree for efficient point queries
- Precompute cluster boundaries from find_fish_clusters output
- Use probe_solution for fast iterative refinement
- Only call evaluate_solution ONCE per restart with the best candidate
- Total time: < 2.0s, aim for 1.5s safety margin
