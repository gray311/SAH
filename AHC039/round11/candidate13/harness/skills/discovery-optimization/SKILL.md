---
name: discovery-optimization
description: "KD-tree enhanced geometric optimization. Use KD-tree for fast spatial queries, try rectangle grid search and expanding vertex strategies, perform deep edge perturbation with \u00b15..15 shifts, validate all candidates, and exploit the fact that edge points count as inside."
---

# KD-Tree Enhanced Polygon Optimization

## Core Strategy

Use the KD-tree built from all fish positions for efficient O(log N) spatial queries. The seed program already has this; enhance the polygon generation around it.

## Phase 1: KD-Tree Construction
- Read all N mackerels and N sardines
- Build KD-tree alternating axes (x, y, x, y, ...)
- Store point indices, track which are mackerels vs sardines

## Phase 2: Polygon Generation (Try Multiple)

### Method A: Rectangle Grid Search
- Extract all unique x-coords and y-coords from fish
- Add midpoints between adjacent unique coords
- For each pair (x_min, y_min, x_max, y_max) from a sparse sample:
  * Decompose into canonical rectangles
  * Score using KD-tree rectangle queries
  * Track best

### Method B: Expanding Vertex Start
- Pick 4-8 seed points (prefer mackerels with few nearby sardines)
- Expand in cardinal directions, forming a growing polygon
- Use KD-tree to efficiently score during expansion

### Method C: Shaped Polygons
- Generate L, U, C shapes by combining rectangular regions
- Be aware of sardine clusters to avoid

## Phase 3: Deep Search
- 5-10 different strategies
- 5-15 random restarts
- Edge perturbation: shift each vertex by ±5, ±10, ±15 units
- Use KD-tree for fast re-scoring after each perturbation
- Try adding vertices at fish positions or interesting grid points

## Phase 4: Edge Exploitation
- Since points on edges count as inside:
  * Deliberately align polygon edges to pass near mackerel clusters
  * Add "padding" around dense mackerel regions
  * Consider thin corridors that just graze mackerel positions

## Phase 5: Validation
- 4 <= vertices <= 1000
- Integer coordinates in [0, 100000]
- Perimeter <= 400,000
- No self-intersection (use standard algorithm)

## Implementation Notes
- Use the existing KD-tree structure from seed, enhance it
- Rectangle query in KD-tree: decompose rectangle into canonical rectangles, sum counts
- Time budget: 2.0s - use efficiently with early termination
- Output: m, then m lines of vertex coordinates
