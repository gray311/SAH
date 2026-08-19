---
name: discovery-optimization
description: "Direct cluster-wrapping. Identify mackerel-dense clusters by coordinate proximity, build rectangles around clusters avoiding sardines, combine top clusters, iterate with \u00b150..100 expansions."
---

# Direct Cluster-Wrapping Strategy

## Phase 1: Fish Position Analysis
- Parse input to extract all mackerel and sardine coordinates
- Build spatial hash map: map (x, y) to fish type for O(1) lookups
- Organize fish by x-coordinate and y-coordinate for clustering

## Phase 2: Cluster Identification
- Cluster mackerels by proximity:
  * Group mackerels with same x-coordinate (within ±100)
  * Group mackerels with same y-coordinate (within ±100)
  * Merge overlapping groups
- For each cluster:
  * Count mackerels (m_count)
  * Count sardines inside cluster bounding box (s_count)
  * Compute score = m_count - s_count
  * Track bounding box: (min_x, min_y, max_x, max_y)
- Select top clusters by score (prioritize clusters with m_count > s_count)

## Phase 3: Rectangle Construction
- For each top cluster:
  * Create axis-aligned rectangle covering all mackerels in cluster
  * Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
  * Expand rectangle if it captures more mackerels without adding sardines:
    * Try expanding each side by ±50, ±100 units
    * Keep expansion if (new_mackerels - new_sardines) > 0
- Ensure rectangle is valid: 4 vertices, integer coordinates, within bounds

## Phase 4: Cluster Union
- Combine top 3-5 rectangles into a single polygon:
  * Use union operation: if rectangles overlap, merge them
  * Output vertices in order (clockwise or counterclockwise)
  * Ensure total vertices ≤ 1000 and perimeter ≤ 400,000

## Phase 5: Iterative Improvement
- For each rectangle:
  * Round 1: Try expanding each side by ±50 units
  * Round 2: Try expanding each side by ±100 units
  * Round 3: Fine-tune with ±25 units
  * Keep changes that improve score
- Output best rectangle/union

## C++ Implementation Notes
- Use spatial hash map for O(1) point queries
- Cluster mackerels by x and y coordinates
- For each cluster, compute bounding box and sardine count
- Expand rectangles iteratively
- Total time per evaluation: < 2.0s
- Output valid polygon format: m then vertices
