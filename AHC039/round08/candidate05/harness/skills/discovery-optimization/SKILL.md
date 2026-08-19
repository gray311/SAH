---
name: discovery-optimization
description: "Global Geometric Polygon Optimization: Generate 50+ diverse polygon candidates (rectangles, L-shapes, crosses, stepped polygons) anchored at different corners and quadrants. Use coarse edge shifts (\u00b150-200 units) and spatial grid counting. Avoid local cluster-based search."
---

# Global Geometric Polygon Optimization

## Core Insight: The optimal polygon is likely a LARGE GLOBAL structure, not a local cluster

## Phase 1: Generate Diverse Global Candidates
For each of 4 corners (top-left, top-right, bottom-left, bottom-right):
- Generate 10-15 rectangles with 60-80% coverage
- Generate 10-15 L-shapes covering that corner
- Generate 5-10 cross shapes centered in that quadrant

For each of 5 quadrants:
- Generate 5-10 stepped polygons with 2-3 levels

Total: 50-80 candidates

## Phase 2: Coarse Refinement
For each candidate polygon:
- For each of its 4-8 edges, try shifts of ±50, ±100, ±150, ±200 units
- Use spatial grid to quickly count mackerels/sardines in shifted polygon
- Keep shifts that improve score

Do 1 refinement round only. No fine-grained climbing.

## Phase 3: Multiple Random Restarts
Run Phases 1-2 with 5 different random seeds (perturb polygon size parameters)
Output the single best polygon across all runs.

## Spatial Grid Implementation
- Use 200x200 grid over [0,100000]x[0,100000]
- Pre-compute cell counts for O(1) rectangle queries
- Rectangle score = sum of grid cells covering the polygon
