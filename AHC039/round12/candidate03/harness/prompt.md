You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL: The solution MUST be correct and compile for ALL 150 test cases. Any invalid output or crash scores 0.

STRATEGY - Simple Grid-Based Rectangle Optimization:

1. GRID BUILD (fast, O(N)):
   - Build 200x200 grid over [0,100000]x[0,100000] with cell_size=500
   - For each cell, count mackerels (M) and sardines (S)
   - Precompute prefix sums for O(1) rectangle queries

2. FIND HIGH-SCORE RECTANGLES:
   - Try rectangles defined by grid cell boundaries
   - Score = sum(cell_scores) for all cells in rectangle
   - Use prefix sums for instant scoring

3. RECTANGLE ENUMERATION:
   - Enumerate rectangles anchored at high M-S cells
   - Try all combinations of (min_row, max_row, min_col, max_col)
   - Filter by perimeter constraint and vertex limit

4. EDGE TUNING:
   - For promising rectangles, try small adjustments (±5, ±10) to corners
   - Re-score using prefix sums

5. VALIDATION:
   - Always ensure output: 4 <= vertices <= 1000, perimeter <= 400,000
   - All coordinates in [0,100000]
   - Simple non-self-intersecting check for axis-aligned rectangles

6. MULTIPLE RESTARTS:
   - Run 10-15 restarts with different random seeds
   - Each: pick random high-M cell, enumerate rectangles, tune edges
   - Output best valid rectangle found

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing above
- evaluate_solution: Run C++ program, get score
- probe_solution: Can be used with grid-based rectangle scoring
- finish: Submit when you have a working solution

Preserve EVOLVE-BLOCK markers and exact I/O format (m then vertices). Ensure <2.0s execution.
KEY: Correctness first - if polygon is invalid, score is 0 for ALL test cases.
