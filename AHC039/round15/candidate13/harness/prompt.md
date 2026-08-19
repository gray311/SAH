You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Brute-force rectangle position search over exact fish coordinates.

SEARCH METHOD:

1. DIRECT COORDINATE ANALYSIS:
   - Read all fish coordinates exactly from input (mackerels and sardines)
   - Build exact position maps (no grid approximation)

2. BRUTE-FORCE RECTANGLE SEARCH:
   - Enumerate all unique x and y coordinates from fish positions
   - Create candidate rectangles from coordinate pairs
   - For each rectangle: compute mackerels - sardines inside
   - Track best score

3. ENLARGEMENT HEURISTICS:
   - Start from high-scoring rectangles
   - Expand in 4 directions (N,S,E,W) by 1-20 units
   - Stop when score stops improving or perimeter constraint hit

4. MULTI-RESTART WITH TIME BUDGET:
   - Run 5-8 restarts with different starting points
   - Each restart: pick random coordinate pairs, build initial rectangle, expand
   - Total time: < 1.8s to leave margin

5. VALIDATION:
   - Output valid axis-aligned polygon (4+ vertices, integer coords, perimeter <= 400,000)
   - Ensure no self-intersection

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ brute-force rectangle search
- evaluate_solution: Run C++, get score
- probe_solution: Not available - need full evaluation for exact scoring
- finish: Submit best polygon

KEY DIFFERENCE from seed: Use exact coordinate enumeration instead of grid approximation.
Try thousands of rectangle positions directly, then refine with local expansion.
