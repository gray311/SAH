You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Use grid-based local search with strategic polygon modifications.

PHASE 1 - GRID SETUP:
- Parse fish positions into a 200x200 grid (cell_size=500)
- For each cell, compute M (mackerels), S (sardines), score = M - S

PHASE 2 - POLYGON INITIALIZATION:
- Start with a minimal valid polygon (4 vertices: a rectangle)
- Center it on the highest-score positive cell
- Ensure perimeter <= 400,000 and coords in [0,100000]

PHASE 3 - LOCAL SEARCH (core innovation):
For up to 500 iterations or until time:
  a) Try expanding polygon in each direction (N,S,E,W) by 1-20 units
  b) Try shrinking each edge
  c) Try rotating corners (90 degree pivots)
  d) Try "flip" moves: replace a vertex with a grid point that improves score
  e) For each candidate, use grid-based rectangle sum for fast scoring
  f) Accept if score improves
  g) Occasional random restart with 2-4 starting cells

PHASE 4 - VALIDATION:
- Output valid polygon (4-1000 vertices, axis-aligned edges)
- Verify perimeter and coordinate constraints
- Score = max(0, mackerels_inside - sardines_inside + 1)

KEY: Use grid for O(1) cell queries, not point-by-point checks. Each evaluation ~1.5s.
