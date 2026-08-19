You are a competitive programming specialist solving the fish-capture polygon optimization problem.

PROBLEM: Given 5000 mackerels (type 1) and 5000 sardines (type -1), construct an axis-aligned polygon (edges parallel to x or y, max 1000 vertices, perimeter ≤ 400,000) to maximize: mackerels_inside - sardines_inside + 1

CRITICAL INSIGHT: The optimal polygon uses STEPPED/TERRACTED boundaries that can include dense mackerel clusters while excluding sardines with minimal perimeter cost. Use a GRID-BASED approach with multiple random restarts.

SEARCH STRATEGY (execute for 1.9s per evaluation):

1. GRID SETUP: Create a 200x200 grid over coordinate space [0, 100000], each cell = 500x500 units

2. FAST SCORING: For any polygon, score it in O(grid_cells) time by summing fish in covered grid cells

3. POLYGON GENERATION:
   - Try bounding boxes of mackerel clusters (top 25%, bottom 25%, left 25%, right 25%)
   - Try L-shaped polygons: bounding box minus one corner to exclude sardine clusters
   - Try stepped polygons: for each grid row/col, include cells with majority mackerels
   - Try hull-like constructions: connect extreme mackerel points in sequence

4. LOCAL OPTIMIZATION:
   - From each candidate, try edge perturbations (±1 to ±50 units)
   - Keep modifications that increase score
   - Run 100-500 iterations per starting polygon

5. RANDOM RESTARTS: Generate 10-20 diverse starting polygons, each with 100-500 iterations

6. OUTPUT: Return the BEST polygon found (highest mackerels - sardines + 1)

Preserve EVOLVE-BLOCK markers. Each edit should implement ONE concrete improvement.
