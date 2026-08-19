---
name: discovery-optimization
description: "Direct coordinate-based clustering for mackerel enrichment. Parse fish coords, use 100x100 grid (cell_size=1000) to find mackerel-dense cells, build minimal bounding boxes around clusters, combine into single polygon, local vertex optimization, 10 restarts."
---

# Direct Coordinate-Based Clustering Strategy

## Phase 1: Direct Input Parsing
- Read N mackerels and N sardines with exact coordinates
- Store in separate vectors for precise spatial queries

## Phase 2: Fine-Grid Clustering
- Use 100x100 grid with cell_size=1000 (covers 0-100000)
- For each cell, collect all mackerel and sardine coordinates
- Compute mackerel density and bounding box per cell

## Phase 3: Cluster Selection
- Select top 5-10 cells with highest mackerel count
- For each selected cell, compute bounding box of all mackerels in that cell
- If multiple mackerels fall in same cell, they get clustered together

## Phase 4: Bounding Box Construction
- For each cluster, create minimal axis-aligned rectangle
- Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- Score each rectangle: count mackerels inside (use point-in-rectangle) minus sardines inside

## Phase 5: Polygon Combination
- Try combining 1-5 clusters by taking their union (overall bounding box)
- Compute union bounding box of selected rectangles
- Ensure: 4 vertices, perimeter <= 400,000, coords in [0, 100000]

## Phase 6: Local Vertex Optimization
- For each vertex, try shifts: ±10, ±20 units
- Use efficient point-in-polygon counting (sweep-line or grid cache)
- Keep shifts that improve score
- Repeat 2 rounds

## Phase 7: Multiple Restarts
- Run 10 restarts with different random seeds
- Each restart: randomly perturb cluster selection, rebuild, optimize
- Output best polygon across all restarts

## Implementation Notes
- Use fast point-in-rectangle tests: (min_x <= x <= max_x) && (min_y <= y <= max_y)
- Pre-process sardines for O(1) range sum queries if needed
- Total time per evaluation: < 2.0s
- Include KVH validator for self-intersection check (though rectangles don't self-intersect)
