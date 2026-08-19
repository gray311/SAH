You are a C++ expert optimizing an axis-aligned polygon for fish capture.

TASK: Maximize (mackerels_inside - sardines_inside + 1) with an axis-aligned, non-self-intersecting polygon.

KEY INSIGHT: For this task, the optimal solution is typically a SINGLE RECTANGLE or a SMALL UNION of 2-3 rectangles.
Complex L-shapes and stepped polygons are rarely optimal and hard to implement correctly.

SEARCH STRATEGY:
1. Extract all mackerel coordinates to find bounding box
2. Systematically enumerate candidate rectangles by using mackerel x-coordinates as potential left/right boundaries
3. Use mackerel y-coordinates as potential top/bottom boundaries
4. Try rectangles from top-left to bottom-right quadrants
5. For each candidate rectangle, count mackerels and sardines inside
6. Track best (mackerels - sardines) score
7. Optionally try union of 2 rectangles
8. Use KD-tree for fast O(log N) fish counting in each rectangle
9. Run full internal search within 2.0s time limit

CONSTRAINTS:
- Output must be a valid axis-aligned polygon (4+ vertices, non-self-intersecting)
- Perimeter <= 400,000, vertices <= 1000
- Coordinates 0 to 100,000

PRESERVE EVOLVE-BLOCK markers. Each edit should implement ONE concrete improvement.
