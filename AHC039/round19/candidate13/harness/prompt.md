You are a C++ polygon optimizer for the fish capture problem. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Cluster-based minimal bounding boxes.

SEARCH METHOD:

1. CLUSTER DETECTION (fine-grained):
   - Read all mackerel coordinates from input
   - Use spatial hashing or grid (100x100 cells of 1000x1000) to find dense mackerel clusters
   - A cluster = group of mackerels within 500 units distance
   - Group mackerels into clusters using Union-Find on proximity

2. CLUSTER-BASED POLYGON CONSTRUCTION:
   - For each mackerel cluster, compute its axis-aligned bounding box (min_x, max_x, min_y, max_y)
   - Create a minimal polygon around each cluster (rectangle with 4 vertices)
   - If clusters are close (< 300 units), consider merging them or adding narrow connecting corridors

3. COMBINATION STRATEGIES:
   a) Single cluster polygon: Use the bounding box of the largest mackerel cluster
   b) Multi-cluster polygon: Union of bounding boxes for top k clusters (k=3-5)
   c) Corridor-connected: Connect nearby clusters with thin corridors (1 unit width)

4. LOCAL OPTIMIZATION:
   - For each polygon, try small expansions in 4 directions (±5, ±10, ±15 units)
   - If expansion captures more mackerels without adding sardines, accept it
   - Try adding "ears" (small rectangles) to capture isolated mackerels

5. MULTIPLE SEARCH PATTERNS:
   - Pattern A: Largest single cluster bounding box
   - Pattern B: Top 3 clusters merged (union of their boxes)
   - Pattern C: Top 5 clusters with thin corridors between adjacent ones
   - Pattern D: All mackerels' convex hull approximation (using minimal axis-aligned rect)

6. VALIDATION & OUTPUT:
   - Ensure 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
   - Ensure axis-aligned edges (only horizontal and vertical segments)
   - Output single best polygon found

Tools:
- edit_solution: Replace EVOLVE-BLOCK with cluster-based minimal bounding box strategy
- evaluate_solution: Run C++ program and get score
- probe_solution: Not needed for this problem
- finish: Submit when you have a working cluster-based approach
