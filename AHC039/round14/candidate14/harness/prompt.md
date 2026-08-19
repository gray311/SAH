You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Coordinate-space rectangle expansion with 2D prefix sums.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. FISH GRID INDEXING:
   - Create coordinate-to-fish mapping for O(1) lookup
   - For any point (x,y), query count of mackerels/sardines in axis-aligned rectangle
   - Use 2D prefix sums for fast rectangle queries after O(N) preprocessing

2. DENSE CLUSTER DETECTION:
   - Identify high-density mackerel regions by scanning x-coordinates
   - For each unique x-coordinate range [x, x+500], count mackerels in [0,100000]x[0,100000]
   - Also track sardine counts for penalty calculation

3. RECTANGLE CONSTRUCTION (key innovation):
   - Start from each dense mackerel cluster center
   - Expand rectangle RIGHT (increase x) as long as: perimeter_growth < 200000 AND new cell has net gain or low penalty
   - Expand rectangle DOWN (increase y) similarly
   - Track best rectangle at each expansion step
   - Try all 4 corner-starting expansion directions

4. PERIMETER-AWARE GROWTH:
   - For rectangle from (min_x, min_y) to (max_x, max_y): perimeter = 2*(max_x-min_x + max_y-min_y)
   - Must stay <= 400,000
   - Each expansion step: try expanding one side by 5, 10, 25, 50, 100 units
   - Evaluate each candidate rectangle using prefix sum queries

5. MULTI-RECTANGLE COMBINATION:
   - Try combining 2-3 non-overlapping rectangles into single polygon
   - Calculate combined perimeter and total score
   - Ensure no self-intersection (rectangles must be axis-aligned and non-overlapping)

6. DEEP LOCAL SEARCH:
   - For each candidate rectangle, try vertex perturbations: ±5, ±10, ±25, ±50 on each corner
   - Use prefix sum queries for fast scoring (no full fish iteration)
   - Keep best perturbations

7. MULTIPLE RESTARTS:
   - Run 10-12 restarts with different starting points
   - Each restart: pick random x-range, build rectangle, refine
   - Total time per eval: < 1.8s to allow margin

8. VALIDATION:
   - Ensure 4 vertices, integer coordinates in [0,100000], perimeter <= 400000
   - Output format: m\n x0 y0\n x1 y1\n ...

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing this strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: Not needed - use fast prefix sum queries internally
- finish: Submit when working
