You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Cluster-focused polygon construction with sardine avoidance.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. SPATIAL ANALYSIS:
   - Read all fish coordinates from input
   - Identify mackerel-dense regions using a spatial histogram (e.g., 500x500 grid, 200x200 cells)
   - For each cell, compute: mackerel_count, sardine_count, density_ratio = M/(M+S) if M+S>0 else 0

2. CLUSTER DETECTION:
   - Find top 20 mackerel-dense cells (highest M count)
   - For each, mark as "cluster center"
   - Identify cells to AVOID: where sardine_count > 5 OR density_ratio < 0.3

3. POLYGON CONSTRUCTION (key innovation):
   - For each cluster center, build a minimal enclosing rectangle:
     * Expand only 50-100 cells in each cardinal direction
     * STOP when hitting: sardine-dense cell (S>5), grid boundary, or another cluster
     * Create 4-sided axis-aligned polygon from rectangle corners
   - Combine clusters: if two cluster rectangles are close (<150 cells apart), merge them into a single larger polygon
   - Output 4-1000 vertices, ensure no self-intersection

4. MINIMAL DISTURBANCE REFINEMENT:
   - For each polygon edge, try shifts of ±10, ±20, ±30 units ONLY
   - Evaluate using grid-based rectangle query (sum M-S in affected area)
   - Accept shift only if it increases net score
   - Max 2 refinement rounds

5. STRATEGIC RESTARTS:
   - Run 8-10 restarts (not 15-20, too many)
   - Each restart: pick random subset of top 10 cluster centers
   - Build minimal rectangles, merge nearby ones
   - Apply minimal refinement

6. VALIDATION:
   - Ensure perimeter <= 400,000, all coords in [0,100000]
   - Vertices: 4-1000, distinct coordinates, axis-aligned edges

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing above strategy
- evaluate_solution: Run C++ program, get score (mackerels-sardines+1)
- probe_solution: Not useful - need accurate scoring
- finish: Submit best polygon found

Key difference from seed: Use minimal enclosing rectangles around mackerel clusters with aggressive sardine avoidance, instead of broad corridor expansion. Focus on tight fits around dense mackerel regions.
