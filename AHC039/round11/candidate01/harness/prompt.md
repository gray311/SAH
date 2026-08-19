You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL: The C++ code must compile and run within ~2.0s per evaluation.

SEARCH STRATEGY (encodes in EVOLVE-BLOCK C++ code):

1. INITIAL POLYGON: Start with a simple axis-aligned polygon that captures all mackerels if possible.
   A good start is the bounding box of all mackerels, extended slightly.

2. EDGE EXTENSION (key innovation): For each edge, try extending it outward by 10, 20, 50, 100 units
   to capture more fish or reduce perimeter. Keep extensions that improve score.

3. HOLE FILLING: If sardines are inside, try "notching" out small rectangular cutouts around them.

4. REFINEMENT: For each vertex, try moving it by ±5, ±10, ±20 units along x or y axis.

5. MULTI-LOBED POLYGONS: Combine multiple rectangular regions into one valid polygon using
   corridor-like connections.

6. MULTIPLE RESTARTS: Run 10-15 restarts with different initial polygons (bounding box variations,
   different corner seeds).

7. VALIDATION: Always output valid polygon (4-1000 vertices, perimeter ≤ 400,000, coords in [0,100000]).

Use edit_solution to replace EVOLVE-BLOCK with complete C++ implementing this strategy.
Use evaluate_solution to get score. Use expand_polygon to try simple mutations.
Use finish when you have a working solution.
