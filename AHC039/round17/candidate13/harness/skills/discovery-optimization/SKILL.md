---
name: discovery-optimization
description: "Cluster mackerels spatially, build bounding boxes, exclude sardine clusters, fine-tune coordinates, multi-strategy exploration."
---

# Clustering-Based Polygon Construction

## Phase 1: Spatial Clustering
- Read mackerel coordinates from input
- Sort by x-coordinate, then group points within 5000-unit windows
- Within each group, sort by y-coordinate, split into clusters of ~20 points
- For each cluster, compute axis-aligned bounding box

## Phase 2: Bounding Box Construction  
- For each cluster's bounding box [x1,y1] to [x2,y2]:
  * Create initial rectangle with 4 vertices
  * Count mackerels (all in cluster + nearby) and sardines inside
  * Score = mackerels - sardines

## Phase 3: Sardine Exclusion
- Check sardine distribution in proposed polygon area
- If sardine density > threshold, either:
  * Split into multiple disjoint rectangles (connected by thin bridges if needed)
  * Offset the bounding box toward lower-sardine areas
  * Make polygon irregular to avoid dense sardine regions

## Phase 4: Coordinate Fine-Tuning
- For each edge of each rectangle:
  * Try outward expansions: +10, +20, +30, +40, +50 units
  * Try inward contractions: -5, -10, -15, -20 units  
  * Keep the best expansion/contraction per edge
- Repeat 2 refinement rounds

## Phase 5: Vertex Perturbation (for small polygons)
- For polygons with <100 vertices:
  * For each vertex, try 4 directional shifts: (±10, 0), (∓10, 0), (0, ±10), (0, ∓10)
  * Also try diagonal: (±10, ±10) for small perturbations
  * Evaluate each variant, keep top 5-10

## Phase 6: Multi-Strategy Evaluation
- Strategy A: Cluster-based bounding boxes (default, 5-10 clusters)
- Strategy B: Single large L-shaped polygon covering top 5 clusters
- Strategy C: Concentric rectangle approach
- Run all strategies, output best result

## Implementation Notes
- Use efficient point-in-rectangle tests
- Pre-compute sorted fish lists for O(log N) queries
- Total time per eval: <2.0s, use multiple restarts (8-12) with different clusterings
