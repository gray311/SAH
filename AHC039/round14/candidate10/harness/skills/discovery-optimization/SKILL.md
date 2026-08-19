---
name: discovery-optimization
description: "Direct geometric optimization for axis-aligned polygons. Read fish coordinates, build fine grid (100x100, cell_size=1000), detect mackerel clusters, construct polygons via expanding boundaries, optimize edges with \u00b15..25 shifts, 10 restarts."
---

# Direct Geometric Polygon Optimization

## Phase 1: Input Parsing
- Read N=5000 mackerels and N=5000 sardines from stdin
- Store as two vectors: mackerels[], sardines[]

## Phase 2: Fine Grid Construction
- Use 100x100 grid with cell_size=1000 (covers 0-100000)
- For each cell, store: vector<int> mackerel_indices, sardine_indices
- Build bounding boxes for cells with fish

## Phase 3: Cluster Detection
- Identify "dense" mackerel cells: those with >= 10 mackerels
- For each dense cell, compute bounding box of all mackerels in it
- Also compute cell's mackerel-sardine score

## Phase 4: Polygon Construction via Expanding Boundaries
For each dense cluster (up to 10):

a. Start with minimal bounding rectangle of mackerels in the cluster

b. Iterative expansion (expanding boundary strategy):
   - Try expanding each of 4 edges by 1, 2, 3, 5, 10 units outward
   - For each candidate expansion:
     * Compute new polygon
     * Count mackerels inside (points where 0 <= x <= max_x and 0 <= y <= max_y, etc.)
     * Count sardines inside
     * Score = mackerels - sardines
     * Accept if score improves
   - Try shrinking edges by 1, 2, 5 units (to exclude sardines on boundary)

c. Build multi-lobed polygon by combining adjacent clusters:
   - If two clusters' bounding boxes overlap or are close, merge them
   - Take union of their polygons

d. Ensure validity:
   - 4 <= vertices <= 1000
   - perimeter <= 400,000
   - coordinates in [0, 100000]

## Phase 5: Local Search Refinement
For each polygon candidate:
- For each edge:
  * Try shifting edge outward by 5, 10, 15, 20, 25 units in each of 4 directions
  * Try shifting edge inward by 5, 10, 15 units
  * Use grid-based counting for fast scoring (sum cells covering polygon)
  * Accept if improves score
- Repeat 3-5 refinement rounds

## Phase 6: Multiple Restarts
- Run 10 restarts with different random seeds
- Each restart: pick random dense cluster, build polygon, optimize
- Track best polygon across all restarts

## Phase 7: Output
- Output vertex count m
- Output m lines of coordinates
- If multiple polygons, last one counts

## Key Optimizations
- Use grid for O(1) approximate counting during expansion
- Final exact count before output
- Avoid recomputing from scratch: use incremental updates
