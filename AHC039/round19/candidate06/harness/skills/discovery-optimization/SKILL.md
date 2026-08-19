---
name: discovery-optimization
description: "Cluster-based rectangle construction. Sort mackerels by x/y, find dense clusters via gap detection, build rectangles around clusters, combine adjacent rectangles, local search with coarse expansions \u00b1500..1500, 25 restarts."
---

# Cluster-Based Rectangle Construction Strategy

## Core Idea
Instead of grid-based corridor expansion, directly cluster mackerels and build compact rectangles around dense regions.

## Phase 1: Cluster Detection
- Sort all mackerels by x-coordinate
- Find gaps > 20000 units between consecutive mackerels
- Group mackerels into x-clusters (groups with gaps <= 20000)
- Repeat for y-coordinate to get y-clusters

## Phase 2: Rectangle Construction
- For each (x_cluster, y_cluster) pair, construct bounding box:
  * min_x, max_x from x_cluster
  * min_y, max_y from y_cluster
  * This gives a candidate rectangle
- Count mackerels and sardines inside each rectangle
- Filter: keep rectangles with score = M - S + 1 >= 2 (i.e., M >= S + 1)

## Phase 3: Multi-Rectangle Combinations
- Sort rectangles by score (descending)
- Try combining top 2-5 rectangles that:
  * Are close to each other (distance < 20000)
  * Don't overlap excessively
- Combine by taking union of all rectangles
- Ensure: vertices <= 1000, perimeter <= 400,000

## Phase 4: Local Search (Coarse)
For each candidate rectangle:
- For each side (left, right, bottom, top):
  * Try expanding: ±500, ±1000, ±1500 units (respecting bounds)
  * Try shrinking: same amounts
  * Use fast rectangle query to count fish
  * Keep changes that improve score
- Repeat up to 2 rounds

## Phase 5: Multiple Restarts
- Run 25 restarts with different parameters:
  * Random gap threshold: 10000 to 30000
  * Random subset of top rectangles to combine
  * Random perturbations to cluster boundaries (±500)
- Track best polygon across all restarts

## C++ Implementation Notes
- Use O(N log N) sorting for clustering
- Use efficient rectangle queries (pre-sorted fish arrays for binary search)
- Fast scoring: O(k log N) per rectangle where k = number of rectangles to evaluate
- Total time per evaluation: < 1.5s to allow margin
- Output exactly one valid polygon (no extra text)
