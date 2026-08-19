You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CORE STRATEGY: Cluster-based rectangle formation around mackerel groups.

SEARCH METHOD:

1. SPATIAL CLUSTERING:
   - Read all mackerel coordinates from input
   - Group nearby mackerels into clusters using DBSCAN-like approach (min_dist=150)
   - For each cluster, find its bounding box (min_x, max_x, min_y, max_y)

2. RECTANGLE CONSTRUCTION:
   - For each cluster, create an axis-aligned rectangle with:
     * Top-left: (min_x-10, min_y-10)
     * Bottom-right: (max_x+10, max_y+10)
     * This creates a small margin around the cluster

3. SARDINE FILTERING:
   - For each candidate rectangle, count sardines inside
   - If sardine_count > 0 and mackerel_count < 5, skip this rectangle (too many penalties)
   - Otherwise, keep it

4. RECTANGLE COMBINATION:
   - Merge overlapping rectangles into larger polygons
   - If non-overlapping, optionally combine adjacent ones into larger shapes
   - Ensure final polygon has 4-1000 vertices and perimeter <= 400,000

5. OUTPUT:
   - Single best polygon (highest mackerels - sardines)
   - Format: m followed by m vertex coordinates

KEY DIFFERENCE from seed: Use fine-grained spatial clustering (not coarse grid) to identify tight mackerel groups, then build rectangles around them while filtering out sardine-rich areas.
