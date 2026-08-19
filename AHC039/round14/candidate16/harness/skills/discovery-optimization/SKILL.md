---
name: discovery-optimization
description: "Coordinate-focused rectangle packing. Parse fish coordinates, find dense mackerel cells, try axis-aligned rectangles around clusters, combine multiple rectangles, local search refinement, 20-30 restarts."
---

# Coordinate-Focused Rectangle Packing Strategy

## Phase 1: Input Analysis
- Parse all N mackerel and N sardine coordinates from input
- Build sparse spatial index (grid cell_size=100 or quadtree)
- Count M and S in each cell, compute density metrics

## Phase 2: Candidate Rectangle Generation
For each cell with high mackerel density:
- Try rectangles of various sizes covering the cell
- Prefer rectangles where M >> S (ideally S=0 in or on boundary)
- Rectangle dimensions: vary from small (covering 1 cell) to large (multiple cells)
- Ensure: integer coords, perimeter <= 400,000, 4-1000 vertices

## Phase 3: Multi-Rectangle Combination
- Combine 2-10 disjoint rectangles into a single polygon
- Option A: Union rectangles into complex axis-aligned polygon
- Option B: Create single enclosing rectangle for multiple clusters
- Option C: Create multi-holed polygon (outer boundary + inner holes for sardine clusters)

## Phase 4: Local Search Refinement
For each candidate:
- Shift polygon centroid by ±50, ±100 units
- Expand/contract individual edges by multiples of 100
- Try splitting large polygons into smaller components
- Try merging nearby polygons
- Use spatial index for O(1) or O(log n) scoring during search

## Phase 5: Multiple Restarts
- Run 20-30 restarts with different random seeds
- Each restart: independently generate 50-100 rectangle candidates
- Evaluate top 10-20 candidates per restart
- Track global best across all restarts

## Phase 6: Output
- Format: m (vertices), then m lines of coordinates
- Clockwise or counterclockwise order
- Ensure valid output even on failures (fallback to seed or simple polygon)
