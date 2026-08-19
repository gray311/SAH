You are a C++ polygon optimizer for axis-aligned fish capture.
Goal: maximize (mackerels - sardines + 1) inside a simple axis-aligned polygon.

STRATEGY: Iterative polygon refinement with population-based search.

PHASE 1: INITIALIZATION
- Parse fish coordinates from input
- Build efficient spatial index (grid/quadtree) for O(1) fish counting in rectangles
- Create initial population of 5-10 candidate polygons:
  * Rectangle covering all mackerels
  * Rectangle from (0,0) to (100000,100000)
  * Random axis-aligned rectangles (20-100 vertices)
  * Cross-shaped polygons centered at mackerel clusters

PHASE 2: SEARCH LOOP (run until time limit ~1.9s)
For each candidate polygon:
  - Evaluate its score using spatial index
  - If score > best, update best
  - Generate 3-5 mutants:
      * Shift one edge by ±5, ±10, ±15 units
      * Add a vertex at a nearby mackerel location
      * Remove a redundant collinear vertex
      * Merge two nearby edges
      * Split a long edge into two segments

POPULATION MANAGEMENT:
- Keep top 10 polygons across all candidates
- Elite preservation: always keep the best 5
- Mutate the rest with diversity constraints (limit vertex overlap)

VALIDATION:
- Each polygon must have 4-1000 vertices
- All vertices in [0, 100000]x[0, 100000]
- Total perimeter <= 400,000
- No self-intersection (check with cross-product or ray casting)
- Output vertices in order (CW or CCW)

OUTPUT: Best polygon found. Format: m (vertices) then m lines of "x y".

TIME CONSTRAINT: Must complete within 1.9 seconds per evaluation.
Use efficient spatial indexing and prune unpromising branches early.
