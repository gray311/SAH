You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The seed program already has a KD-tree for spatial queries. Don't waste time on coarse grid-based approaches. Instead:

SEARCH METHOD:

1. HIGH-RESOLUTION INPUT ANALYSIS:
   - Parse input to get ALL fish coordinates exactly
   - Build spatial index (KD-tree or quadtree) for O(log N) point-in-polygon queries
   - Compute density maps at fine resolution (not 500x500 cells)

2. CLUSTER-BASED POLYGON CONSTRUCTION:
   - Find dense mackerel clusters using spatial clustering (DBSCAN-like)
   - For each cluster, build a minimal bounding rectangle
   - Compute score for each rectangle using exact fish counting
   - Combine rectangles into larger polygons if beneficial

3. DIRECTED HILL CLIMBING:
   - Start from promising rectangles/clusters
   - For each edge, try small expansions in 4 directions: ±10, ±20 units
   - Use spatial index for fast O(N) rectangle scoring
   - Keep improvements up to 100 iterations

4. STRATEGIC RESTARTS:
   - Run 8-10 restarts (not 15-20)
   - Each restart: pick random subset of top 50 mackerels, build enclosing rectangle
   - Diversify by using different random seeds and starting regions

5. VALIDATION:
   - Ensure 4-1000 vertices, perimeter ≤ 400,000, coords in [0,100000]
   - Use proper axis-aligned polygon rules (no self-intersection by construction)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with precise geometric construction strategy
- evaluate_solution: Run C++ program, get exact score
- analyze_fish_distribution: NEW - get high-res fish density map and cluster info
- probe_solution: NOT useful - full evaluation needed

Key difference from seed: Use spatial clustering on exact coordinates, build tight rectangles around dense mackerel groups, use KD-tree for efficient scoring, fewer but smarter restarts.
