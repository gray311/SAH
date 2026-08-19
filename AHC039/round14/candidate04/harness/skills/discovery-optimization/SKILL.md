---
name: discovery-optimization
description: "Exact spatial clustering + KD-tree: read all fish coordinates, cluster mackerels spatially, build KD-tree for O(log N) queries, construct polygons around clusters, hill climb with \u00b110..50 shifts, 25+ restarts."
---

# Exact Spatial Clustering and KD-Tree Optimization
## Phase 1: Exact Input Reading
CRITICAL: Read 2N coordinates directly from input: - Lines 1-2N: coordinates of N mackerels (x, y) - Lines N+1-2N: coordinates of N sardines (x, y) - Store in two vectors: mackerels and sardines
## Phase 2: Spatial Indexing
Build a KD-tree or grid-based spatial hash of ALL 2N fish: - Each node stores bounding box and fish count - Supports O(log N) rectangle range queries - Use std::nth_element for median-of-medians in KD-tree construction
## Phase 3: Mackerel Cluster Discovery
Using scan_mackerel_clusters tool: - Get list of mackerel-dense regions (centroid, extent) - Each region: min_x, max_x, min_y, max_y (bounding box)
## Phase 4: Candidate Polygon Construction
For each region from step 3: 1. Create axis-aligned rectangle from (min_x, min_y) to (max_x, max_y) 2. Query KD-tree: exact mackerel count (should be region size) 3. Query KD-tree: exact sardine count (penalty) 4. Score = mackerels - sardines + 1
## Phase 5: Multi-Region Union
Combine multiple region rectangles: - Union of bounding boxes (expanded to cover all) - Re-query KD-tree for exact counts in union - Compute score - Ensure perimeter <= 400,000
## Phase 6: Hill Climbing
For each candidate polygon with M edges: - For each edge i: * Try shifts: ±10, ±20, ±30, ±40, ±50 units (larger exploration!) * Shift creates new polygon, re-query KD-tree * Keep shift maximizing score - Repeat 4 refinement rounds
## Phase 7: Multiple Restarts
- Run 30 restarts with different random cluster selections - Each restart: pick 3-10 random mackerel clusters, build candidate, hill climb - Output best polygon across all restarts
## Implementation Notes
- Fast I/O: ios::sync_with_stdio(false), cin.tie(nullptr) - KD-tree: balance to ensure O(log N) queries - Time budget: < 2.0s per evaluation - Output: m (vertices), then m lines of (x, y) coordinates
