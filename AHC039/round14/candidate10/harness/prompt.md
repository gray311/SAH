You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. INPUT PARSING:
   - Read N=5000 mackerel coordinates and N=5000 sardine coordinates from stdin
   - Store all points in separate vectors

2. SPATIAL INDEXING:
   - Build a 100x100 grid (cell_size=1000) over [0,100000]x[0,100000]
   - For each cell, store list of mackerel and sardine indices in that cell
   - Also maintain bounding box for each cell

3. CLUSTER DETECTION:
   - Find dense mackerel regions: cells with mackerel_count >= 10
   - For each dense cell, compute the bounding box of all mackerels in it

4. POLYGON CONSTRUCTION (Key Innovation - Direct Geometric Approach):
   - Start with a simple axis-aligned polygon enclosing one dense mackerel cluster
   - Use "expanding boundary" strategy: 
     * Begin with minimal rectangle covering the cluster
     * Iteratively expand in each of 4 directions by 1-10 units
     * After each expansion, count mackerels (inside or on boundary) and sardines
     * Accept expansion if it increases (mackerels - sardines)
   - Support multi-lobed polygons: repeat expansion from multiple cluster centers
   - Merge overlapping polygons by taking union

5. EDGE OPTIMIZATION:
   - For each edge, try expanding/shrinking by 5, 10, 15, 20, 25 units in all 4 directions
   - Accept move if it improves score and maintains validity
   - Repeat 3-5 rounds

6. MULTIPLE RESTARTS:
   - Run 10 restarts with different starting clusters
   - Each restart builds a polygon from scratch and optimizes

7. VALIDATION:
   - Ensure 4 <= vertices <= 1000
   - Ensure perimeter <= 400,000
   - All coordinates in [0, 100000]
   - No self-intersection (axis-aligned polygons naturally satisfy this if constructed carefully)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run program, get score
- probe_solution: NOT useful - need exact count
- finish: Submit best polygon
