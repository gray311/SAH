You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Direct dense-region targeting with simple rectangular/L-shaped polygons.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. SPATIAL INDEXING:
   - Build a spatial grid (e.g., 50x50 or 100x100 cells) over [0,100000]x[0,100000]
   - For each cell, count mackerels (M) and sardines (S)
   - Compute density score = M - S

2. REGION SELECTION:
   - Find top 5-10 cells with highest positive (M-S) score
   - Use these as seed regions for polygon construction

3. POLYGON CONSTRUCTION (SIMPLIFIED):
   - From each seed cell, build a rectangle or L-shaped polygon
   - Rectangle: expand in all 4 directions by same amount
   - L-shape: expand 2+ directions from corner
   - Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]

4. MINIMAL HILL CLIMBING:
   - For each candidate, try small edge shifts: ±1, ±2, ±3 units
   - Keep shifts that improve the score
   - 1-2 refinement rounds only

5. LIMITED RESTARTS:
   - Run 3-5 restarts with different random seeds
   - Each restart: pick 3 seed cells, build polygons, hill climb

6. VALIDATION:
   - Output valid polygon only
   - Check perimeter and coordinate bounds

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get score (budget=30 evals)
- probe_solution: Use for rapid iteration (cheap approximate scoring)
- finish: Submit best solution found

KEY DIFFERENCE: Simpler construction, smaller shifts, fewer restarts = faster per-eval execution under 2.0s.
