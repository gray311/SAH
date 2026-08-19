---
name: discovery-optimization
description: "Direct coordinate-based density analysis. Scan coordinates at fine granularity, find dense mackerel clusters, expand rectangular regions in best direction, track M-S counts exactly, many random restarts."
---

# Direct Coordinate-Based Density Analysis Strategy

## Core Idea

Instead of coarse grid cells, analyze fish distribution at the coordinate level to find optimal rectangular regions.

## Phase 1: Coordinate-Level Analysis
- Work with coordinates at their natural scale (0-100,000)
- For efficiency, use a spatial index (quadtree, sorted lists by x and y)
- Identify regions with high mackerel density

## Phase 2: Region Expansion
For each dense mackerel region:
- Start with a small rectangle around the densest fish
- Try expanding in 4 directions: increase x_max, increase y_max, decrease x_min, decrease y_min
- For each expansion, count all fish inside the new rectangle
- Keep the expansion that gives the best M-S score
- Stop when no expansion improves the score

## Phase 3: Multi-Region Combination
- Try combining multiple disjoint rectangles into a single polygon
- Or output a single large rectangle that encompasses multiple clusters
- Ensure valid polygon (4 vertices for a rectangle)

## Phase 4: Multiple Restarts
- Run 20-30 restarts, each starting from a different dense mackerel region
- Track the best polygon across all restarts
- Output the single best result

## Implementation Notes
- Use efficient spatial queries (avoid O(N*M) nested loops)
- Pre-sort fish by x and y coordinates
- Use prefix sums or 2D range queries for fast rectangle counting
- Total time per evaluation: < 2.0s
