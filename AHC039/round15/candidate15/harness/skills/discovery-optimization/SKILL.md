---
name: discovery-optimization
description: "Direct geometric local search. Build fine grid (50x50, cell_size=2000), use prefix sums for O(1) rectangle queries, perform iterative vertex insertion/deletion/shift with coarse then fine phases, optimize vertex count, single focused optimization."
---

# Direct Geometric Local Search Strategy

## Phase 1: Fine Grid Construction
- Use 50x50 grid over [0,100000]x[0,100000] (cell_size=2000)
- For each cell, count mackerels and sardines
- Compute 2D prefix sums for O(1) rectangle score queries

## Phase 2: Initial Polygon
- Find dense mackerel cluster (cell with highest M, or highest M-S)
- Create minimal axis-aligned bounding box around it (4 vertices)

## Phase 3: Coarse Local Search (200 iterations)
For each iteration:
- Try vertex insertion: pick random grid boundary point, insert vertex, compute delta via prefix sum
- Try vertex deletion: if >4 vertices, remove random vertex, compute delta
- Try vertex shift: pick random endpoint, shift by ±[1,5,10,20,40] in x or y, compute delta
- Keep best mutation if score improves

## Phase 4: Fine Local Search (100 iterations)
- Same operations but with finer shifts: ±[1,2,3,4,5] units

## Phase 5: Vertex Count Optimization
- Try polygons with 4, 5, 6, 8, 10, 12, 16 vertices
- For each count, run local search from random seed
- Keep best result

## Phase 6: Final Validation
- Check perimeter <= 400,000
- Check coords in [0,100000]
- Check 4 <= vertices <= 1000
- Check no self-intersection (non-adjacent edges don't share points)

## Key Success Factors
- Fine grid (cell_size=2000) for accurate fish counting
- Prefix sums for O(1) rectangle queries
- Iterative local search beats grid-based corridor expansion
- Single focused optimization invests more time per variant
