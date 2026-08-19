You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Use grid-based cluster analysis with KD-tree spatial indexing to find mackerel-rich regions, then construct tight bounding boxes around high-value clusters with minimal sardine contamination.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER DETECTION (Fast):
   - Read fish coordinates, separate mackerels from sardines
   - Use 2D spatial indexing (grid 500x500 cells or KD-tree) to quickly identify regions with high mackerel density and low sardine density
   - For each grid cell, compute score = M - S, track top 30 cells

2. CLUSTER BOUNDING BOX CONSTRUCTION:
   - For each high-value cell (score >= 0 or S/M ratio < 0.5), collect all mackerels in that cell
   - If cell has mackerels, build minimal axis-aligned bounding box that contains ONLY that cell's mackerels
   - Compute perimeter: if 4*cell_size <= 400000, accept; else skip
   - For larger clusters, try decomposing into smaller adjacent high-value cells

3. EXPONENTIAL CONTOUR EXPANSION (Key Innovation):
   - From each cluster's bounding box center, try expanding to adjacent 8 neighbors
   - For each direction (N,S,E,W and diagonals), check if adjacent cell has better M-S ratio
   - Expand greedily as long as: 
     * New cell has M >= S or (M > 0 and S < M + 3)
     * Perimeter growth < 5000 units
     * Total perimeter <= 390000 (safety margin)
   - Track 8-directional contours, form convex-like polygons

4. EXPONENTIAL REFINEMENT:
   - For each candidate polygon, try edge shifts of ±5, ±10, ±15, ±20, ±25, ±30 units in 8 directions
   - Use grid-based scoring for each shifted variant (O(1) query)
   - Keep shifts that improve M - S by at least 0.5, break ties with perimeter reduction
   - Repeat 4 refinement rounds (compounding small improvements)

5. MULTI-SCALE RESTARTS:
   - Run 25-35 restarts with different seeds
   - Each restart: 
     * Randomly perturb grid cell selection by ±1..3 cells
     * Build 4-8 bounding boxes from top cells
     * Try merging adjacent boxes if union is still valid (no self-intersection)
     * Perform exponential refinement

6. VALIDATION:
   - Ensure 4 <= vertices <= 1000, integer coordinates, no self-intersection
   - Check perimeter <= 400000, all coords in [0,100000]
   - Use bounding box construction to guarantee axis-aligned property

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing above strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: Approximate scoring useful for quick variant ranking (score reliability: 0.7-0.85 on dense clusters)
- finish: Submit when you have 35+ restarts, exponential refinement, and bounding-box construction

PRESERVE EVOLVE-BLOCK markers, exact I/O format (m then vertices), and ensure <2.0s execution.

KEY DIFFERENCE from seed: Use grid clustering + bounding boxes + exponential contour expansion instead of corridor expansion. Focus on tight cluster capture rather than long narrow corridors.
