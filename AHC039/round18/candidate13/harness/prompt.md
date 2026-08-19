You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Direct coordinate-based clustering and bounding box construction.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. DIRECT COORDINATE PARSING:
   - Read all fish coordinates directly from stdin (no grid approximation)
   - Store mackerels and sardines in separate vectors with their exact coordinates

2. SPATIAL CLUSTERING (key innovation):
   - Use a 100x100 grid with cell_size=1000 (finer than seed's 500)
   - For each cell, compute bounding box of all fish in that cell
   - Find cells with highest mackerel density (mackerels per cell)
   - For each high-density cell, build minimal axis-aligned bounding box around ALL mackerels in that cell

3. SMART BOUNDING BOX CONSTRUCTION:
   - For each cluster of mackerels, compute min_x, max_x, min_y, max_y
   - Check if building a rectangle around this cluster captures enough mackerels while excluding sardines
   - Score = (mackerels_inside - sardines_inside)

4. POLYGON COMBINATION:
   - Try combining 1-5 clusters into a single polygon by taking their union (rectangular merge)
   - Use union of axis-aligned rectangles: compute overall bounding box of selected clusters
   - Ensure resulting polygon has 4-1000 vertices and perimeter <= 400,000

5. LOCAL OPTIMIZATION:
   - For each vertex of the polygon, try small perturbations (±10, ±20)
   - Use KD-tree or grid for fast point-in-polygon queries
   - Keep perturbations that improve score

6. MULTIPLE RESTARTS:
   - Run 10 restarts with different cluster selection strategies
   - Each restart: random sample of top cells, build bounding boxes, combine, optimize

7. VALIDATION:
   - Ensure polygon is simple (no self-intersection)
   - All coordinates in [0, 100000]
   - Output format: m followed by m lines of vertices
