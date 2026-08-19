You are a C++ rectangle optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

KEY INSIGHT: The optimal solution is likely a rectangle (4 vertices) enclosing a dense mackerel cluster while avoiding sardines.

SEARCH METHOD (must run in ~1.5s per evaluation):

1. READ INPUT: Parse N mackerels and N sardines with exact coordinates.

2. BUILD KD-TREE: Organize all fish by coordinate for fast O(log N) range queries.

3. RECTANGLE SEARCH:
   - Start with seed rectangle (minimum bounding box of all fish)
   - For each evaluation, generate 50-100 candidate rectangles by:
     * Randomly sampling 2-4 candidate vertex coordinates from fish positions
     * Clustering: find dense mackerel regions and test rectangles around them
     * Edge shifting: perturb rectangle boundaries by ±10, ±20, ±50 units
   - Score each candidate using KD-tree rectangle query: sum mackerels inside minus sum sardines inside
   - Use O(1) update: track rectangle and incrementally update score as edges move

4. HILL CLIMBING:
   - For top 10 best rectangles, try local refinements:
     * For each of 4 edges, try 10 position shifts
     * Score each using rectangle query
     * Keep best refinement
   - Repeat 2-3 rounds

5. OUTPUT: Return best rectangle (4 vertices) that satisfies constraints (4 vertices, perimeter ≤ 400,000, coords in [0,100000]).

Preserve EVOLVE-BLOCK markers, exact I/O format, and ensure <2.0s execution. The seed program has working KD-tree and rectangle query infrastructure - reuse and enhance it, don't replace with grid-based approaches.
