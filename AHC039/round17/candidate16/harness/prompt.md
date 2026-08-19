You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

KEY INSIGHT: The optimal solution likely uses small, tight axis-aligned rectangles around dense mackerel clusters.

SEARCH STRATEGY (encodes in EVOLVE-BLOCK C++ code):

1. READ INPUT: Parse all fish positions (5000 mackerels, 5000 sardines).

2. BRUTE-FORCE SMALL RECTANGLES (most promising):
   - Try all rectangles of size 1x1, 1x2, 2x1, 2x2, 3x3 around each mackerel
   - For each rectangle, count enclosed mackerels (M) and sardines (S)
   - Score = M - S + 1 (only if M >= S)
   - Track best rectangle

3. EXPAND SUCCESSFUL RECTANGLES:
   - If a rectangle scores well, try expanding it by 1 unit in each direction
   - Continue expansion while score improves

4. TRY MULTI-RECTANGLE SOLUTIONS:
   - Try combining 2-3 non-overlapping rectangles
   - Score as sum of individual rectangle scores

5. LARGE RECTANGLE SEARCH (fallback):
   - If small rectangles don't beat the seed, try larger rectangles (up to 100x100)
   - Sample 100 random center points, expand to capture nearby fish

6. VALIDATION:
   - Ensure 4 <= vertices <= 1000, perimeter <= 400,000, integer coords in [0,100000]
   - Output valid polygon

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing rectangle search
- evaluate_solution: Run C++ program, get score
- probe_solution: Use for quick testing of candidate rectangles before full eval
- finish: Submit when you have a working rectangle search

CONSTRAINTS: Total time < 2.0s per evaluation. Prioritize small rectangles (O(1) counting) over large ones.
