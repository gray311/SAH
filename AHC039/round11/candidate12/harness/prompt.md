You are a C++ solver for the axis-aligned fish capture problem.
Goal: Construct a polygon (axis-aligned edges only) to maximize (mackerels_inside - sardines_inside + 1).

CONSTRAINTS:
- 4 to 1000 vertices
- Perimeter ≤ 400,000
- Integer coordinates in [0, 100000]
- No self-intersection

STRATEGY (use these steps to generate the EVOLVE-BLOCK C++ code):

1. GRID-BASED FISH COUNTING:
   - Create a grid of cell_size=200 (500x500 cells covering 0-100000)
   - Count mackerels and sardines in each cell
   - Precompute prefix sums for O(1) rectangle scoring

2. RECTANGLE SEARCH:
   - Try all axis-aligned rectangles on the grid
   - Score = (mackerel_count - sardine_count + 1)
   - Track top 100 rectangles by score

3. RECTANGLE MERGING:
   - Merge adjacent rectangles if combined polygon has better score
   - Limit to 2-3 merged rectangles (complexity grows quickly)

4. POLYGON CONSTRUCTION:
   - Convert merged rectangles to vertex list
   - Ensure valid axis-aligned polygon (track perimeters)

5. SEARCH LOOP (REQUIRED):
   - Implement iterative improvement: try random rectangle perturbations
   - Use simulated annealing or simple hill climbing
   - Run for up to 10000 iterations within time limit
   - Track best solution found

6. TIME BUDGET:
   - Must complete in < 1.9 seconds
   - Use efficient data structures (prefix sums, grid arrays)
   - Avoid O(N²) geometry checks; use grid-based queries only

OUTPUT FORMAT:
  m
  a_0 b_0
  a_1 b_1
  ...
  a_{m-1} b_{m-1}

CRITICAL: The C++ code must be syntactically valid, properly formatted with escaped newlines (\\n), and implement the above strategy.
