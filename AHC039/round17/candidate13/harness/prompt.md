You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTERING: 
   - Read all mackerel coordinates from input
   - Cluster mackerels using simple spatial grouping (group points within 5000 units)
   - For each cluster, compute the axis-aligned bounding box

2. BOUNDING BOX CONSTRUCTION:
   - For each cluster's bounding box [min_x, max_x] x [min_y, max_y]:
     * Start with a rectangle covering all points in that cluster
     * Check if this rectangle captures most mackerels and few sardines

3. SARDINE AVOIDANCE:
   - Before finalizing any polygon, query sardine positions in the proposed region
   - If a large sardine cluster overlaps (>30% sardines), split the polygon or offset it
   - Use coordinate-based checks (not grid approximation)

4. POLYGON MEGALOMANIA:
   - Connect nearby bounding boxes with rectangular bridges (sharing edges when possible)
   - Or build a single large polygon covering multiple clusters if beneficial
   - Ensure: 4 <= vertices <= 1000, perimeter <= 400,000

5. COORDINATE-FINE TUNING:
   - For each polygon edge, try expanding by ±10, ±20, ±30, ±40, ±50 units in outward direction
   - For each edge, try contracting by ±5, ±10, ±15, ±20 units in inward direction
   - Use fast point-in-polygon tests with pre-read sardine/mackerel positions
   - Keep modifications that increase (mackerels - sardines)

6. BRUTE-FORCE LOCAL SEARCH:
   - For small polygons (<100 vertices), try vertex coordinate perturbations:
     * Each vertex: try ±10, ±20, ±30 in x and y (4 directions per vertex)
     * Limited to top 5-10 best variants per parent polygon

7. MULTIPLE STRATEGIES:
   - Strategy A: Cluster-based bounding boxes (default)
   - Strategy B: Single large polygon covering ~80% area if mackerel density is high
   - Strategy C: Concentric rectangles (outer rectangle for mackerels, inner holes blocked by sardines)
   - Run all 3, pick best score

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing clustering + bounding boxes + coordinate fine-tuning
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - need exact counts
- finish: Submit when you have working clustering-based approach with coordinate tuning

Key difference from seed: Use spatial clustering of mackerels + coordinate-based sardine exclusion + direct coordinate perturbations instead of grid corridors.
