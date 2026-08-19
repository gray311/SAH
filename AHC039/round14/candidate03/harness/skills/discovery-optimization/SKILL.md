---
name: discovery-optimization
description: "Fish capture optimizer using spatial grid indexing for fast polygon scoring. Build polygon with axis-aligned edges, use 2D grid hash table for O(vertices) scoring, optimize via hill climbing and multiple restarts."
---

# Spatial Grid-Based Polygon Optimization

## Phase 1: Build Spatial Index
- Create a 2D grid (e.g., 100x100, cell size 1000) covering [0,100000]×[0,100000]
- For each fish (mackerel or sardine), increment the count in its cell
- This enables fast area queries by summing cell counts over polygon cells

## Phase 2: Polygon Construction Strategies
Choose one of these approaches:

### Strategy A: Rectangle with Lobes
- Start with a minimum bounding rectangle of mackerels
- Add rectangular "lobes" in cardinal directions (N,S,E,W)
- Each lobe: extend polygon in one direction, stop when marginal gain is negative

### Strategy B: Morphological Operations
- Start with a seed polygon (e.g., bounding box of top 20% mackerels)
- Apply dilation (expand outward) or erosion (shrink inward)
- Use grid to quickly evaluate each morphed variant

## Phase 3: Fast Scoring with Spatial Grid
- For a polygon with axis-aligned edges, decompose into elementary rectangles
- For each rectangle, sum grid cells it covers (O(vertices) time)
- This is 10-100x faster than O(N) point-in-polygon for N=10000 fish

## Phase 4: Hill Climbing
- For each edge (x1,y1)-(x2,y2):
  * Try shifts: ±1, ±2, ±5 units perpendicular to the edge
  * Use incremental grid-based scoring (recompute only affected cells)
  * Keep shift that improves score
- Repeat 5-10 rounds until no improvement

## Phase 5: Multiple Restarts
- Run 5-10 restarts with:
  * Different starting rectangles (randomly perturbed mackerel clusters)
  * Different lobe combinations
  * Different morphological operations
- Output the best polygon from all restarts

## Implementation Notes
- Grid cell size: 1000 (gives 100x100 grid, 10,000 cells)
- Polygon scoring: decompose into O(vertices) elementary rectangles
- Time budget: <2.0s per evaluation, prioritize quantity of variants
- Self-intersection: use simple rectangle-based construction to avoid
