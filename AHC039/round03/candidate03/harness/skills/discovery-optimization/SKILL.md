---
name: discovery-optimization
description: "Optimize orthogonal polygon construction by implementing internal search that probes many variants\nbefore evaluation. Use coordinate-based strategies and probe_solution for cheap ranking."
---

# Orthogonal Polygon Construction - Method Guide

## Understanding the Task
- N=5000 mackerels and sardines each
- Score = max(0, mackerels_inside - sardines_inside + 1)
- Polygon must be axis-aligned orthogonal (edges parallel to x or y)
- Vertices must be integers 0-100000, distinct coordinates, non-self-intersecting

## Construction Strategies to Try

Strategy A: Bounding Box with Cutouts
- Find min/max x and y of ALL fish (bounding rectangle)
- This captures ALL fish but includes all sardines too
- Make a hole by indenting edges to exclude sardine clusters
- Iterate: try different indent positions and depths

Strategy B: Cluster-Based Multiple Polygons
- Cluster mackerels by proximity
- For each cluster, build a tight orthogonal polygon around it
- Combine into a single valid polygon

Strategy C: Coordinate Grid Construction
- Collect all unique x and y coordinates from fish
- These form a natural grid; polygon edges should align with this grid
- Sort unique x's: x1 < x2 < ... < xk
- Sort unique y's: y1 < y2 < ... < yl
- Construct polygon that includes points in certain grid cells

Strategy D: Perimeter-Based Expansion
- Start with a small polygon around a mackerel
- Expand the polygon by 1 unit in cardinal directions
- Only expand if net gain > 0 (add mackerel, don't add sardine)
- Keep expanding until perimeter budget exhausted

Strategy E: Greedy Rectangle Packing
- Find dense mackerel regions
- Build axis-aligned rectangles around them
- For each rectangle, compute mackerels vs sardines
- Keep rectangles with positive contribution

Internal Search Pattern
- For each evaluation:
  - candidates = []
  - for strategy in [A, B, C, D, E]:
      - for variant parameter in [10 variations]:
          - polygon = construct_polygon(strategy, variant)
          - score = probe_solution(polygon)
          - candidates.append((score, polygon))
  - best = max(candidates, key=lambda x: x[0])
  - output = best[1]
  - evaluate_solution()

## Implementation Details
- Time limit: ~2.0s per evaluation with 0.1s safety margin
- With 1.9s, you can afford 50-100 internal iterations if each is O(1)
- Each probe takes ~10ms, so 200 probes = 2s (budget edge)
- Aim for 50-100 iterations: 10ms each = 1-1.5s

## Optimization Tips
- Use KD-tree or grid for O(log N) point queries inside your search
- Cache results when rebuilding polygons
- Prune search: if a partial polygon already has negative net, abandon
- Use coordinate hashing to quickly check which cells are included

## Self-Correction
- If score is low: your polygon construction is wrong or too greedy
- If validity=0: fix self-intersection or coordinate bounds
- If score improves: refine your winning strategy
