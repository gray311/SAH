You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

PROBLEM: Create an axis-aligned polygon (4-1000 vertices, perimeter ≤400,000) that encloses mackerels while avoiding sardines.

SEARCH STRATEGY (geometric rectangle tiling approach):

1. SPATIAL INDEXING:
   - Read all fish positions from input
   - Build a sorted list/hash map for O(1) point lookups
   - For rectangle queries, use inclusion-exclusion with sorted coordinates

2. GRID OF CANDIDATE RECTANGLES:
   - Divide search space into coarse grid (e.g., 100x100 with cell_size=1000)
   - For each grid cell, compute the best axis-aligned rectangle that:
     * Fits entirely within the cell or adjacent cells
     * Has perimeter ≤ 400,000
     * Maximizes (mackerels_in_rect - sardines_in_rect)

3. RECTANGLE COMBINATION:
   - Combine adjacent high-scoring rectangles into valid polygons
   - Ensure no self-intersection and valid vertex ordering
   - Total perimeter must stay under limit

4. RECTANGLE SCORING WITH PROBE:
   - Use probe_solution to quickly test rectangle candidates
   - Only call evaluate_solution on promising polygons
   - Score = #mackerels - #sardines + 1 (if negative, score = 0)

5. ITERATIVE REFINEMENT:
   - Start with small rectangles around dense mackerel clusters
   - Expand rectangles in 4 directions, tracking when sardines appear
   - Split large low-scoring rectangles into smaller high-scoring ones
   - Merge adjacent rectangles if they form better combined score

6. MULTIPLE START STRATEGIES:
   - Strategy A: Find dense mackerel clusters, grow rectangles around them
   - Strategy B: Sweep-line approach, finding local maxima of density
   - Strategy C: Random seed points, grow until sardine limit
   - Run 10-15 strategies, output best valid polygon

CRITICAL RULES:
- All vertex coordinates must be integers in [0, 100000]
- Polygon must be simple (no self-intersection)
- Vertices with collinear consecutive points are allowed
- Output format: m (vertex count) then m lines of "x y"

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing the above
- evaluate_solution: Full evaluation, count fish inside polygon
- probe_solution: Use for quick rectangle score estimates (subsample ~10% of fish)
- new_tool count_fish_in_rect: Query mackerels and sardines in any rectangle [x1,y1] to [x2,y2]
- new_tool density_grid: Build coarse grid of fish density for fast exploration
