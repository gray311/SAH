You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

KEY STRATEGY: Compact rectangle construction around mackerel clusters.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER-BASED APPROACH:
   - Read mackerel coordinates from input
   - Use simple 1D projection clustering: sort mackerels by x-coordinate, find gaps > 20000 units
   - For each cluster of mackerels (x-range < 20000), treat as a potential rectangle candidate
   - Similarly cluster by y-coordinate

2. RECTANGLE CONSTRUCTION:
   - For each x-cluster and y-cluster pair, construct a candidate rectangle
   - Rectangle corners: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
   - Filter: only consider rectangles with >= 4 mackerels inside and <= 2 sardines
   - Compute score = mackerels_inside - sardines_inside + 1

3. MULTI-RECTANGLE COMBINATIONS:
   - Try combining adjacent rectangles (sharing an edge or close to each other)
   - For combinations, ensure total perimeter <= 400,000 and vertices <= 1000
   - Use union of rectangles to form complex axis-aligned polygons

4. LOCAL SEARCH:
   - For each candidate rectangle/combo:
     * Try expanding each side by ±500, ±1000, ±1500 units (coarse steps)
     * Try shrinking each side by same amounts
     * Keep changes that improve score
   - Max 2 refinement rounds

5. MULTIPLE RESTARTS:
   - Run 25 restarts with different random perturbations
   - Each restart: different gap threshold (10000-30000), different combination strategy
   - Track best polygon across all restarts

6. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords in [0,100000])
   - Perimeter <= 400,000, no self-intersection

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing cluster-based rectangle construction
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed for accurate scoring
- finish: Submit when you have encoded a working cluster-based rectangle optimizer
