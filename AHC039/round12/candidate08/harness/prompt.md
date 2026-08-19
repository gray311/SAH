You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Simple greedy expansion with KD-tree queries and local refinement.

SEARCH METHOD (encode in EVOLVE-BLOCK C++ code):

1. READ INPUT: Parse mackerel and sardine coordinates from stdin.

2. BUILD KD-TREE: Build KD-tree on all fish points for O(log N) range queries.

3. INITIAL POLYGON: Start with a minimal valid polygon (e.g., small rectangle around centroid).

4. GREEDY EXPANSION: 
   - Query score for current polygon
   - Try expanding each edge by ±1, ±5, ±10 units
   - Keep expansion that improves score
   - Max 50 expansion steps total

5. LOCAL HILL CLIMBING:
   - For each edge, try vertex perturbations ±2, ±5, ±10
   - Keep improvements
   - Max 10 iterations

6. OUTPUT: Valid polygon (4-1000 vertices, perimeter ≤400000, coords in [0,100000]).

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get score
- finish: Submit when you have a working solution

PRESERVE: EVOLVE-BLOCK markers, exact I/O format (m then vertices), <2.0s execution.
Key: Simple is faster. Use existing KD-tree. Avoid complex grid/corridor logic.
