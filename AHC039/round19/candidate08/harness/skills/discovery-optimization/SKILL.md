---
name: discovery-optimization
description: "Direct geometric clustering with tight axis-aligned bounding boxes. Group mackerels into spatial clusters, compute tight AABB for each, combine adjacent clusters, local expansion/shrink, diversified cluster radii."
---

# Direct Geometric Clustering Strategy

## Phase 1: Spatial Clustering
- Read all fish coordinates from input (N mackerels + N sardines)
- For mackerels, group into clusters where distance between points <= 2000
- Use simple proximity clustering: start from unvisited mackerel, BFS to find all within 2000
- Compute tight axis-aligned bounding box for each cluster:
  * min_x, max_x, min_y, max_y from cluster points
  * Perimeter = 2*(max_x - min_x + max_y - min_y) (account for integer coords)

## Phase 2: Sardine Penalty Assessment
- For each cluster's bounding box, count sardines inside
- Use KD-tree for fast point-in-rectangle queries
- Compute score = M - S for each cluster
- Keep clusters with score > 0

## Phase 3: Rectangle Combination
- Sort clusters by score descending
- Try merging adjacent clusters (boxes that overlap or touch)
- For each merge, compute new score (union rectangle)
- Accept merge if score improves
- Handle overlapping rectangles using axis-aligned union

## Phase 4: Local Expansion
- For each retained rectangle, try expanding each side by 50, 100, 150 units
- For each expansion, quickly estimate sardine count (sample or KD-tree)
- Expand only if M_gain > S_gain
- Similarly try shrinking if interior is sardine-dense

## Phase 5: Multi-Cluster Polygon Construction
- Combine multiple rectangles into single valid axis-aligned polygon
- Use sweep-line algorithm for axis-aligned union
- Ensure: 4 <= vertices <= 1000, perimeter <= 400000, coords in [0,100000]
- Validate no self-intersection

## Phase 6: Diversified Search
- Run multiple attempts with different parameters:
  * Cluster radii: 1000, 1500, 2000, 2500
  * Merge strategies: greedy vs exhaustive
  * Expansion sizes: 50, 100, 150
- Track best polygon across all attempts
- Output single best polygon

## C++ Implementation Notes
- Use O(N log N) KD-tree for fast rectangle queries
- Simple proximity clustering (BFS from seed point)
- Axis-aligned union via sweep-line or plane sweep
- Total time per evaluation: < 2.0s
- Include proper error handling for edge cases
