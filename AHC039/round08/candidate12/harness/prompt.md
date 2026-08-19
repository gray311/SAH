You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL: Implement a GLOBAL COORDINATE-SPACE SEARCH that:

1. BUILD A COMPREHENSIVE SPATIAL INDEX:
   - Create a 2D grid (CELL_SIZE=500) over [0,100000]x[0,100000]
   - For each cell, count mackerels (M), sardines (S), and their positions
   - Compute score density = M / max(1, S + 0.1) for each cell
   - Identify HIGH-DENSITY REGIONS: cells with density > threshold (start at 1.0, try higher)

2. GLOBAL RECTANGLE EXPANSION SEARCH:
   - For each high-density region:
     * Start with the region's bounding box
     * GREEDILY expand each edge outward by 50, 100, 150, ... units
     * After each expansion, check: (a) perimeter increase vs (b) score gain
     * Continue expanding while score_gain / perimeter_increase > 0.5
     * Track best rectangle for each region
   - Also try CONTRACTION: shrink each edge inward by 50, 100, ... units to exclude nearby sardines
   - For each candidate, compute final score and validity

3. MULTI-SHAPE POLYGON COMBINATION:
   - Take top 3 rectangles from different regions
   - Try combining them as a union (may require up to 12 vertices)
   - Score the combined shape
   - If score improves, keep it; otherwise use best single rectangle

4. HILL CLIMBING WITH BOUNDARY SMOOTHING:
   - For each edge of the best polygon, try shifting ±1, ±2, ... ±50 units
   - After each shift, verify validity (no self-intersection, perimeter ≤ 400000)
   - Keep shifts that improve score and maintain validity
   - Repeat up to 3 rounds with decreasing step sizes (50, 20, 10)

5. MULTIPLE SEARCH STRATEGIES WITH TIME BUDGET:
   - Run Strategy 1: Global rectangle expansion with 10 random seeds
   - Run Strategy 2: Contraction-focused search (exclude sardines first)
   - Run Strategy 3: Corner-focused search (target corners with high mackerel density)
   - Each strategy spends ~0.4s, stop when time limit reached
   - Output the single best valid polygon across all strategies

Tools:
- edit_solution: Modify C++ EVOLVE-BLOCK with complete global search code
- evaluate_solution: Run program, get score (mackerels-sardines+1)
- probe_solution: Use for quick rectangle score checks before full evaluation
- finish: Submit when you have a working global search

Preserver EVOLVE-BLOCK markers and exact I/O format. Each edit encodes ONE search strategy improvement.
