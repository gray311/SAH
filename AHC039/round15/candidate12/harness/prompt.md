You are a C++ polygon optimizer for axis-aligned fish capture (eft__ahc_simpletes__ahc039).
Goal: maximize (mackerels_inside - sardines_inside + 1).

METHOD: Direct point clustering + greedy polygon growth + local search.

STEP 1 - PARSING:
- Read 2N=10000 points: first N are mackerels (type=1), next N are sardines (type=-1)
- Store in vectors for O(1) access

STEP 2 - SPATIAL GRID FOR LOOKUP:
- Build 1000x1000 grid (cell_size=100) over [0,100000]²
- For each cell: count mackerels (M), sardines (S)
- Compute cell_score = M - S

STEP 3 - FIND SEED POINTS:
- Identify top 8 cells with highest positive cell_score
- Use these as polygon seed locations

STEP 4 - GREEDY POLYGON CONSTRUCTION:
- For each seed cell, create a minimal bounding box around all fish in nearby cells
- Start with 4-vertex rectangle around seed cell
- Try expanding in 4 cardinal directions (N,S,E,W) by adding vertices:
  * New vertex = (current_edge_endpoint_x, new_y) or (new_x, current_edge_endpoint_y)
  * For each expansion candidate, compute exact score (count fish in polygon)
  * Only expand if score increases AND perimeter <= 400000 AND vertices <= 1000
- Combine expansions into valid axis-aligned polygon

STEP 5 - EXACT SCORING:
- Polygon score = count_mackerels_in_polygon - count_sardines_in_polygon + 1
- Point-in-convex-polygon: for axis-aligned, check if point is within bounding box
- For complex polygons: use ray casting or break into rectangles

STEP 6 - LOCAL SEARCH (Hill Climbing):
- For best polygon found, perform 2-3 rounds of local optimization:
  * For each edge, try small shifts: ±3, ±5, ±8, ±12 units
  * Compute exact score for each shifted polygon (rectangle intersection with fish)
  * Keep shifts that improve score
  * Repeat until no improvement

STEP 7 - OUTPUT:
- Output best polygon from all seeds and perturbations
- Format: m (vertex count)\nx0 y0\nx1 y1\n...\n
- Ensure: 4 <= vertices <= 1000, distinct coordinates, integer coords [0,100000]

TIME BUDGET: 2.0s per evaluation. Prioritize speed: use arrays not vectors, avoid dynamic allocations.
