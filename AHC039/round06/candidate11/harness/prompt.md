You are optimizing C++ code for a geometric optimization: maximize (mackerels_inside - sardines_inside + 1) with an axis-aligned polygon.

CRITICAL STRATEGY - Implement a BINARY SEARCH RECTANGLE OPTIMIZER:

ALGORITHM:
1. Read 5000 mackerels and 5000 sardines from stdin
2. Compute mackerel bounding box: [min_x, max_x] x [min_y, max_y]
3. For each of 4 boundaries (left/right/bottom/top), binary search to find the tightest position that maximizes: mackerels_kept - sardines_excluded
4. Choose the best single-sided shrink (greedy)
5. Output 4 rectangle vertices

WHY THIS WORKS:
- O(N) per boundary check, O(N log stride) total
- Completes in ~0.05-0.1s for N=5000, well under 2.0s limit
- Rectangle captures mackerels densely, excludes sardines efficiently

CONSTRAINTS (or validity=0):
- 4 distinct vertices, 0 <= x,y <= 100000, integer
- Axis-aligned edges, perimeter <= 400000
- No self-intersection

If simple rectangle fails, try multi-rectangle, then complex polygon as last resort.

Use probe_solution to test approaches on subsampled data before full evaluation.
