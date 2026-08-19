You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL FAILURE ANALYSIS: The current harness strategy (grid-based corridor expansion) is failing because:
1. Grid granularity (cell_size=500) is too coarse to capture the fine-grained fish distribution
2. Corridor expansion creates thin rectangles that often fail to enclose enough fish
3. The validator (KVH) may be rejecting valid polygons due to implementation bugs
4. Hill climbing on edges is too slow and doesn't explore the search space well

NEW STRATEGY: Use a DIRECT PACKING approach:

1. SORTING-BASED BOUNDARY CONSTRUCTION:
   - Sort all mackerels by x-coordinate, take top K (K=500)
   - Sort all sardines by x-coordinate, take top K (K=500)
   - Create a polygon that encloses the leftmost M mackerels while excluding the leftmost S sardines
   - Use the bounding box of selected mackerels and expand/contract edges to avoid sardines

2. SPECIFIC POLYGON CONSTRUCTION:
   - Find min_x and max_x of top K mackerels
   - Find min_y and max_y of top K mackerels
   - Create a rectangle with corners at (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
   - For each edge, check if any sardines are on it and adjust the edge position to exclude them
   - Expand the rectangle in all 4 directions as long as it captures more mackerels and avoids sardines

3. K-WAY CLUSTERING:
   - Divide the 2D space into a 5x5 grid (20x20 cells)
   - For each cell, count mackerels and sardines
   - Select cells with positive score (M > S)
   - For each selected cell, create a small rectangle that encloses the mackerels
   - Combine these rectangles into a single polygon (union of convex hulls)

4. ADVANCED HILL CLIMBING:
   - Start with the initial polygon
   - For each vertex, try perturbation in 8 directions (N, NE, E, SE, S, SW, W, NW)
   - For each direction, try 3 distance values: 100, 200, 500 units
   - Accept if the new polygon has higher score
   - Repeat until no improvement or max iterations reached

5. TIME-EFFICIENT IMPLEMENTATION:
   - Pre-compute all fish positions into arrays
   - Use binary search to quickly find which fish are inside/outside a polygon
   - Cache polygon score computation
   - Limit the number of hill climbing iterations per eval to keep total time < 2s

6. VALIDATION:
   - Always output a valid polygon (4-1000 vertices, integer coords, perimeter <= 400000)
   - Use simple bounding box check before output
   - Ensure no self-intersection (axis-aligned polygons are simpler)

KEY DIFFERENCE from seed: Instead of grid-based corridor expansion, use direct packing of mackerel clusters with sardine-aware boundary adjustment.
