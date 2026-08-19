You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. START FROM SEED: Load existing polygon, extract edge coordinates and bounding box.

2. LOCAL GRID SCAN: Build a coarse 100x100 grid (cell_size=1000) over [0,100000]x[0,100000].
   For each cell, count mackerels and sardines from input fish data.

3. DIRECTIONAL EXPANSION: For each of the 4 cardinal directions from the seed's bounding box center,
   grow a corridor in that direction for up to 50 cells, stopping if:
     - cell score (M-S) becomes negative
     - sardine count exceeds mackerel count by more than 1
     - grid boundary reached

4. POLYGON CONSTRUCTION: Convert each corridor into a simple rectangle. Combine up to 4
   corridors into a single polygon if they share a common region.

5. MINIMAL HILL CLIMBING: For each candidate polygon, do ONE round of refinement:
   - For each of the 4 outer edges, try shifts of ±5, ±10 units perpendicular to the edge
   - Keep the shift that improves or maintains the score

6. FEW RESTARTS: Run 5-7 restarts with different random perturbations of the starting
   bounding box (±2000 units randomly in each direction).

7. VALIDATION: Ensure 4-1000 vertices, integer coords in [0,100000], perimeter ≤ 400,000.

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing this streamlined strategy
- evaluate_solution: Run C++ program, get score (mackerels-sardines+1)
- probe_solution: Use for quick checks - try probe before full eval if score looks similar
- finish: Submit when you have a working local-search polygon optimizer

KEY DIFFERENCE from current: Simplified grid (100x100 vs 200x200), fewer restarts (5-7 vs 15-20),
smaller shifts (±5,±10 vs ±5..25), single refinement round. This fits within 2.0s C++ time limit.
