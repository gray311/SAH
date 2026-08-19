---
name: discovery-optimization
description: "Geometric cluster union. Group mackerels into clusters by proximity, compute bounding boxes, union them into a stepped polygon, exclude sardines by edge adjustment."
---

# Geometric Cluster Union Strategy

## Phase 1: Parse Input
- Read N from stdin
- Read 2N points: first N are mackerels (type=1), next N are sardines (type=-1)
- Store all points in vectors

## Phase 2: Cluster Mackerels
- Use Union-Find or BFS to group mackerels by proximity
- Distance threshold: 2000 units (tunable)
- For each cluster, compute bounding box:
  * min_x = min x coordinate in cluster
  * max_x = max x coordinate in cluster
  * min_y = min y coordinate in cluster
  * max_y = max y coordinate in cluster
- Store cluster as {min_x, max_x, min_y, max_y, mackerel_count}

## Phase 3: Count Sardines in Each Cluster
- For each cluster bounding box, count sardines inside
- Compute score = mackerel_count - sardine_count
- Sort clusters by score descending

## Phase 4: Union Clusters into Polygon
- Sort clusters by x coordinate
- Merge adjacent/overlapping clusters
- Build stepped polygon by connecting bounding boxes
- Ensure: 4-1000 vertices, perimeter ≤400,000

## Phase 5: Sardine Exclusion
- Check if any sardine lies on polygon edges or inside
- Try expanding box by 1-5 units outward if safe
- Use KD-tree for fast point-in-polygon queries

## Phase 6: Output
- Output m vertices followed by coordinates
- Try multiple strategies (different cluster thresholds, k values)
- Output best polygon

## Time Complexity
- Clustering: O(N log N) with sorting or O(N²) with brute force
- Sardine counting: O(N × number_of_clusters) with coordinate search
- Total should fit in 2.0s for N=5000
