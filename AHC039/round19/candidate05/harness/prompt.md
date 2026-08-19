You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The optimal polygon vertices should be close to actual fish coordinates. Build polygons by:
1. Using mackerel coordinates as seed anchor points
2. Building axis-aligned bounding boxes around clusters of mackerels
3. Expanding/contracting edges incrementally to exclude nearby sardines

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CONFIGURE THE CODE:
   - Include <set> for coordinate deduplication and O(log n) lookup
   - Use integer coordinates throughout
   - Track best score with full precision

2. BUILD FROM FISH COORDINATES:
   - Parse input to extract all mackerel (type=1) and sardine (type=-1) coordinates
   - Store mackerels in a sorted structure for cluster detection
   - Store sardines in a hash set for O(1) membership testing

3. POLYGON CONSTRUCTION PHASES:
   
   A. Single Mackerel Bounding Boxes (baseline):
      - For each mackerel, create a minimal 4-vertex axis-aligned rectangle
      - Rectangle edges: extend 1 unit in each direction from fish coordinate
      - This guarantees the fish is inside
      - Score: count mackerels inside - count sardines inside + 1
   
   B. Cluster-Based Polygons:
      - Group nearby mackerels (within 50 units in both x and y)
      - For each cluster, build a tight bounding box
      - Ensure boxes don't overlap sardine coordinates
      - Merge overlapping clusters into larger polygons
   
   C. Strategic Edge Expansion:
      - Start from cluster bounding boxes
      - For each edge, try expanding OUTWARD by 1-10 units if it captures more mackerels
      - Try contracting INWARD by 1-5 units if it excludes more sardines
      - Use sardine hash set for O(1) density estimation
   
   D. Multi-Cluster Combinations:
      - Try combining 2-3 nearby cluster polygons into one large polygon
      - Use union of bounding boxes (may create non-minimal shapes)
      - Evaluate combined score

4. VALIDATION AND OUTPUT:
   - Ensure 4-1000 vertices, all coordinates in [0, 100000]
   - Ensure perimeter <= 400,000
   - Ensure no self-intersection (axis-aligned polygons are simple if built correctly)
   - Output format: m (vertex count), then m lines of "x y"
   - Always output the BEST polygon found (not first one)

5. SEARCH LOOP:
   - Run 10-15 independent construction strategies
   - Each strategy: different seed, different expansion amounts
   - Keep track of best score across all strategies
   - Use time-budgeted search (stop if 1.85s elapsed)

6. EDGE CASES:
   - If no mackerels inside any polygon, output a minimal valid polygon (4 vertices) at origin
   - Handle boundary conditions (fish at coordinates 0 or 100000)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get score
- probe_solution: Can be used for quick validation of candidate polygons
- finish: Submit when you have working coordinate-space construction

KEY DIFFERENCE from seed: Directly use fish coordinates to build polygons, not grid abstraction. Incremental edge tuning based on actual fish positions.
