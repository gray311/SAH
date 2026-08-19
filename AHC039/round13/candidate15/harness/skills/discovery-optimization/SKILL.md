---
name: discovery-optimization
description: "Direct dense-region targeting. Build spatial grid, find top mackerel-dense cells, construct simple rectangles/L-shapes, minimal hill climb with \u00b11-3 shifts, 3-5 restarts."
---

# Simple Polygon Construction Strategy

## Phase 1: Spatial Grid Analysis
- Build grid (e.g., 50x50 or 100x100) over [0,100000]²
- Count mackerels (M) and sardines (S) per cell
- Score = M - S

## Phase 2: Seed Region Selection
- Pick top 5-10 cells with highest positive score
- These are your mackerel-dense regions

## Phase 3: Simple Polygon Construction
For each seed cell:
- Expand uniformly in 4 directions (rectangle) OR
- Expand 2+ directions from corner (L-shape)
- Use integer coordinates, simple geometry

## Phase 4: Minimal Hill Climbing
- For each edge, try shifts: ±1, ±2, ±3 units
- Use probe for fast scoring
- 1-2 refinement rounds

## Phase 5: Limited Restarts
- 3-5 restarts total
- Each: 3 seed cells → polygons → hill climb → track best

## Implementation Notes
- O(1) grid access after O(N) preprocessing
- Total time per eval: <1.5s for safety margin
- Use KD-tree or grid for fast region queries
