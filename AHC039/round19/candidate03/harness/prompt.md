You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Use binary space partitioning to find optimal axis-aligned polygons that enclose mackerels while avoiding sardines.

SEARCH METHOD:

1. FISH LOADING & STRUCTURING:
   - Parse fish coordinates from task inputs (use ctx.list_task_inputs() or read from program)
   - Store mackerels and sardines in separate vectors

2. BOUNDING BOX CONSTRUCTION:
   - Find min/max x, y for all fish
   - Create bounding box covering all fish

3. GEOMETRIC ANALYSIS & BINARY SEARCH:
   - For each of the 5000 mackerels, consider a square centered at that mackerel
   - This is a better target size than random
   - Use binary search on half-width to find optimal square size

4. OPTIMAL SQUARE SELECTION:
   - Count fish in each candidate square
   - Calculate score = mackerels_in_square - sardines_in_square + 1
   - Keep the top 3 squares

5. POLYGON CONSTRUCTION:
   - For each optimal square, create an axis-aligned polygon with 4 vertices
   - Ensure coordinates are integers in [0, 100000]
   - Ensure perimeter <= 400,000

6. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords, no self-intersection)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing above strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful for polygon scoring - use count_fish_in_square instead
- finish: End when you have a working square-based optimizer

KEY DIFFERENCE from seed: Directly target individual mackerels with geometrically-optimal squares, use binary search to find best size, output simple 4-vertex polygons.
