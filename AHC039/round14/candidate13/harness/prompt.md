You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Direct cluster-based rectangle construction with local sardine exclusion.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER IDENTIFICATION:
   - Read all mackerel positions
   - Use clustering (DBSCAN-like or distance threshold) to find mackerel clusters
   - For each cluster, compute bounding box

2. RECTANGLE CONSTRUCTION:
   - For each cluster, create initial axis-aligned rectangle from bounding box
   - Ensure at least 4 vertices and perimeter <= 400,000
   - Coordinate bounds: [0, 100000]

3. LOCAL SARDINE EXCLUSION:
   - For each rectangle, query all sardine positions inside
   - If sardines found, adjust rectangle corners to exclude them:
     * Shift top/bottom edges past sardine y-coordinates
     * Shift left/right edges past sardine x-coordinates
     * Try multiple corner configurations
   - Use brute-force corner adjustment (±10 units) to minimize sardine inclusion

4. CLUSTER MERGING:
   - Try merging adjacent rectangles into larger polygons
   - Merge if combined perimeter doesn't exceed limit and score improves

5. DEEP LOCAL SEARCH:
   - For each edge, try corner perturbations: ±3, ±7, ±15, ±30 units
   - Evaluate each perturbation by counting mackerels/sardines inside
   - Keep best perturbation, repeat 2-3 rounds

6. MULTIPLE RESTARTS:
   - Run 25-30 restarts with different cluster perturbations
   - Each restart: perturb cluster centers, rebuild rectangles, optimize
   - Output single best polygon

7. VALIDATION:
   - Ensure 4-1000 vertices, integer coords, no self-intersection
   - Perimeter <= 400,000

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run program, get score (budget=30)
- finish: Submit best working solution

Key difference from grid-based approach: Use direct point queries and geometric construction, not coarse grid abstraction.
