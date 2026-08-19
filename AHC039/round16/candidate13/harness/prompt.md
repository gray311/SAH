You are a C++ polygon optimizer for axis-aligned fish capture (NP-hard heuristic problem).
Goal: maximize (mackerels_inside - sardines_inside + 1) for an axis-aligned polygon (edges parallel to x or y axes).

CONSTRAINTS: 4-1000 vertices, perimeter <= 400,000, coords in [0,100000], no self-intersection.

SEARCH METHOD (implement in EVOLVE-BLOCK C++ code):

1. GRID-BASED PREPROCESSING:
   - Build 200x200 grid (cell_size=500) over [0,100000]x[0,100000]
   - For each cell, count mackerels (M) and sardines (S) from input
   - Build 2D prefix sum array for O(1) rectangle queries of M and S counts
   - Compute cell scores = M - S for quick heuristic guidance

2. INITIAL POLYGON CONSTRUCTION:
   - Start with a simple valid polygon: the bounding box of all mackerels
   - If no mackerels exist, start with a small 4-vertex square at (0,0)-(500,500)
   - Ensure valid output format (4-1000 vertices, integer coords, no self-intersection)

3. ITERATIVE POLYGON IMPROVEMENT (simulated annealing style):
   - Run for up to 500 iterations (or until time expires):
     a) Generate candidate mutations:
        * Vertex insertion: add a new vertex on an edge at random position
        * Vertex deletion: remove a vertex if it doesn't break validity
        * Vertex shift: perturb a vertex coordinate by ±50..200 (prefer grid-aligned)
        * Edge expansion: extend an edge outward by 100..500 units in its direction
        * Rectangle merge: combine two adjacent edges into a larger rectangle
     b) For each candidate, compute score using grid-based rectangle query (O(1))
     c) Accept if score improves, or with probability exp((new_score - old_score)/T) where T decreases
     d) Track best polygon found

4. LOCAL HILL CLIMBING (final refinement):
   - From best polygon, run 50-100 edge refinements:
     * For each edge, try expanding outward by 50, 100, 150, 200, 250 units
     * Use grid query to score each variant
     * Keep the best valid expansion
     * Also try vertex jitter: ±10, ±20, ±30 on each vertex
   - Validate final polygon (4-1000 vertices, perimeter check, coordinate bounds)

5. OUTPUT:
   - Single best valid polygon found
   - Format: m (vertices) then m lines of "x y"

CRITICAL: Ensure <2.0s execution. Use prefix sum grid for O(1) scoring.
Prioritize quantity of candidates over deep single-candidate optimization.
All coordinates must be integers in [0,100000].

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing above iterative improvement
- evaluate_solution: Run C++ program, get score (budget=30 evals)
- probe_solution: Not needed - grid-based scoring is already cheap
- finish: Submit best polygon
