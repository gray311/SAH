You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The current grid-based approach is too coarse (500x500 cells). Fish are individual points;
build polygons around actual fish positions, not cell aggregates.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. FISH-BASED CLUSTERING:
   - Parse all fish positions (mackerels and sardines) from input
   - Build a KD-tree or 2D grid with cell_size=50 (10x smaller than before)
   - For each mackerel, find nearby sardines (distance < 100) - these are "conflict points"
   - Group mackerels into clusters based on proximity (distance < 150)

2. CLUSTER-BASED RECTANGLE CONSTRUCTION:
   - For each mackerel cluster:
     * Compute bounding box of cluster
     * Expand bbox by ±20 units to capture edge fish
     * Subtract "conflict" sardines (those inside the expanded bbox)
     * Score = (mackerels in bbox) - (sardines in bbox)
     * If score > 0, keep this rectangle

3. MERRIERS' ALGORITHM (key innovation):
   - Sort all candidate rectangles by score (descending)
   - Greedily select non-overlapping rectangles with highest scores
   - Try to merge adjacent rectangles if combined score improves
   - Handle overlaps by splitting rectangles at overlap boundaries

4. EDGE REFINEMENT (fine-grained):
   - For each selected rectangle, try moving each edge by ±1, ±3, ±5, ±10, ±15 units
   - Use fast O(1) point-in-rectangle queries (not grid-based)
   - Evaluate new rectangle score exactly (count fish individually)
   - Accept if score improves

5. ITERATIVE IMPROVEMENT:
   - After initial selection, try to add small rectangles in gaps between selected ones
   - If adding a rectangle reduces overlap with existing ones, compute adjusted score

6. MULTIPLE STRATEGIES:
   - Strategy A: Largest mackerel clusters first
   - Strategy B: Densest regions first (mackerel density > sardine density)
   - Strategy C: Random seed with local search
   - Run 8 strategies, output best

7. VALIDATION:
   - Ensure 4 <= vertices <= 1000, perimeter <= 400000, coords in [0,100000]
   - No self-intersection (axis-aligned rectangles naturally satisfy this when non-overlapping)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing fish-based clustering
- evaluate_solution: Run C++ program, get exact score
- probe_solution: NOT useful - need exact counts
- finish: Submit when you have encoded working fish-based clustering

KEY DIFFERENCE from current harness: Work with individual fish positions, not coarse grid cells.
This enables precise rectangle placement around actual fish clusters.
