You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Local cluster-based polygon construction with fine-grained edge tuning.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER DETECTION:
   - Read all fish coordinates from input
   - Use spatial hashing or grid (cell_size=100) to find dense mackerel regions
   - For each cell, compute: density = mackerel_count / sardine_count
   - Identify cells with density > 2.0 AND mackerel_count >= 5

2. TIGHT POLYGON CONSTRUCTION:
   - For each high-density cluster, construct a minimal axis-aligned bounding box
   - Ensure: all edges parallel to axes, coordinates in [0,100000], perimeter <= 400000
   - If cluster is small, build a single small polygon (4-8 vertices)
   - If multiple nearby clusters, consider merging with minimal expansion

3. FINE-GRAINED EDGE TUNING:
   - For each polygon edge, try shifts: ±1, ±2, ±3, ±4, ±5 units (not ±5..25!)
   - For each shift, compute the change in mackerel/sardine count by checking nearby fish
   - Keep the shift that maximizes (mackerels - sardines)
   - Repeat 5 refinement rounds with decreasing step sizes: 5, 3, 1, 0.5, 0.25

4. ITERATIVE REFINEMENT LOOP:
   - Start with seed polygon (if valid) or a default 4-vertex polygon
   - For up to 50 iterations:
     * Try 3 mutation types: (a) edge shift, (b) vertex addition, (c) vertex removal
     * Use local fish counting to evaluate each mutation (O(1) with spatial index)
     * Keep mutation that improves score
     * Break if no improvement in 3 consecutive iterations

5. MULTIPLE CLUSTER HANDLING:
   - Try building separate polygons for each top 5 clusters
   - Also try combining top 2-3 clusters with minimal connecting corridors
   - Compare scores and output best

6. VALIDATION:
   - Ensure polygon is valid: 4-1000 vertices, no self-intersection, integer coords
   - Use bounding box checks and simple edge-intersection tests

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing this cluster-based strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed for accurate scoring
- finish: Submit when you have a working cluster-based polygon optimizer

KEY DIFFERENCE from seed: Instead of coarse grid-based corridors, use fine-grained local cluster detection with sub-unit edge tuning and iterative refinement.
