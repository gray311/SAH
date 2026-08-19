You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Grid-based rectangle exploration with sardine boundary optimization.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. GRID-BASED SCAN:
   - Use 100x100 grid (cell_size=1000) over [0,100000]x[0,100000]
   - For each cell, count mackerels (M) and sardines (S)
   - Compute cell score = M - S
   - Identify ALL cells with score > 0 as "candidate regions"

2. RECTANGLE EXPANSION (key innovation):
   - From each candidate cell, expand in all 4 directions
   - Build maximal rectangles that maintain positive net score
   - Rectangle must be valid: 4 vertices, perimeter <= 400,000, integer coords
   - Try different rectangle sizes: small (4x4 cells), medium (10x10), large (50x50)

3. BOUNDARY OPTIMIZATION:
   - For each rectangle candidate, try boundary shifts:
     * Shift right edge by ±1, ±2, ±3 units to exclude sardines on boundary
     * Shift top edge by ±1, ±2, ±3 units similarly
   - Use grid-based scoring to evaluate each variant quickly
   - Keep variant with highest M - S

4. MULTI-RECTANGLE COMBINATION:
   - Try combining 2-3 non-overlapping rectangles into one polygon
   - Use "comb" or "crown" shapes that connect rectangles with corridors
   - Ensure total perimeter and vertex count constraints

5. DEEP HILL CLIMBING:
   - For each top candidate polygon:
     * For each edge (up to 1000), try shifts ±5, ±10, ±15, ±20 units
     * Use grid-based rectangle query for fast scoring
     * Repeat 5 refinement rounds
   - Track best improvement

6. RANDOMIZED START POINTS:
   - Run 25 restarts with different random seed cell selections
   - Each restart: pick 5 random candidate cells, build rectangles from each
   - Combine and hill climb
   - Output single best polygon across all restarts

7. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords in [0,100000])
   - Ensure perimeter <= 400,000 and no self-intersection
   - Use KVH polygon validator

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation of above strategy
- evaluate_solution: Run C++ program, get score
- finish: Submit when you have a working grid-based rectangle explorer

KEY DIFFERENCE from seed/corridor: Systematic rectangle search with boundary optimization, not corridor expansion. Focus on enclosing dense mackerel clusters with sardine-excluding boundaries.
