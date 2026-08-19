You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Direct geometric local search with spatial indexing.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. SPATIAL INDEXING:
   - Build 2D grid over [0,100000]x[0,100000] but with FINE cells (50x50, cell_size=2000)
   - For each cell, count mackerels (M) and sardines (S)
   - Also maintain prefix sums for O(1) rectangle queries

2. LOCAL SEARCH (key innovation over grid corridors):
   - Start from a small initial polygon (e.g., minimal bounding box around dense mackerel cluster)
   - For 200-300 iterations:
     * Try inserting a vertex at random grid cell boundary
     * Try deleting a vertex (if >4 vertices)
     * Try shifting an endpoint by 1-50 units in cardinal directions
     * Use prefix sum query to compute delta score in O(1)
     * Keep mutation if score improves

3. VERTEX OPERATIONS:
   - Insert: add vertex at (rand_x, rand_y) where rand values are multiples of cell_size
   - Delete: remove random vertex
   - Shift: move endpoint by ±[1,5,10,20,40] units in x or y direction

4. MULTI-PHASE REFINEMENT:
   - Phase 1: Coarse search (±1-50 shifts, 200 iterations)
   - Phase 2: Fine search (±1-10 shifts, 100 iterations)
   - Phase 3: Vertex count optimization (try 4, 5, 6, 8, 10, 12, 16 vertices)

5. SINGLE HIGH-QUALITY POLYGON:
   - Instead of 15-20 restarts, do 1 focused optimization run
   - Invest time in thorough local search rather than many shallow attempts
   - Output the best polygon found

6. VALIDATION:
   - Ensure 4 <= vertices <= 1000
   - Ensure perimeter <= 400,000
   - Ensure all coords in [0,100000]
   - Use simple self-intersection check (no two non-adjacent edges share points)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing direct geometric local search
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed
- finish: Submit when you have encoded working local search

KEY DIFFERENCE from seed: Direct vertex manipulation with fine-grained shifts, spatial prefix sums for O(1) scoring, single focused optimization instead of many restarts.
