You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Use coordinate-based rectangular construction from actual fish positions.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. COORDINATE GRID CONSTRUCTION:
   - Extract all unique x and y coordinates from fish positions (mackerels and sardines)
   - Build a coordinate grid where each cell boundary is at an actual fish coordinate
   - This creates a fine-grained grid aligned with fish distributions

2. RECTANGULAR BLOCK ANALYSIS:
   - For each grid cell (rectangle between consecutive unique coords), count mackerels (M) and sardines (S)
   - Compute cell score = M - S
   - Identify cells with positive score (M > S)

3. RECTANGLE CONSTRUCTION:
   - Build rectangles by combining adjacent positive-score cells
   - Try different rectangle sizes (4, 6, 8, 10, 12, 16 vertices) to capture clusters
   - Ensure perimeter <= 400,000 and all coordinates in [0,100000]

4. SIMPLEX HILL CLIMBING:
   - For each candidate rectangle, try expanding in all 4 directions by ±1, ±2, ±3 units
   - Keep expansions that improve M-S count
   - Limit to 2 refinement rounds max

5. MULTIPLE RESTARTS WITH COORDINATE PERTURBATION:
   - Run 8-12 restarts (faster than 15-20)
   - Each restart: randomly select 2-3 adjacent positive cells, build rectangle, hill climb
   - Track best polygon across all restarts

6. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords, no self-intersection)
   - Simple perimeter check (sum of edge lengths)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation of above strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed for accurate scoring
- finish: Submit when you have a working coordinate-based rectangle construction

KEY DIFFERENCE from seed: Use coordinate-aligned rectangles instead of grid-based corridors.
Rectangles are built from actual fish coordinates, enabling precise cluster capture.
Simpler hill climbing (±1..3) saves time for more restarts.
