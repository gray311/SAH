---
name: discovery-optimization
description: "Point-based cluster exclusion. Cluster fish by proximity, build bounding boxes around mackerel-dense regions, avoid sardine-dense regions, merge overlapping boxes, try diverse polygon shapes (rectangles, L-shapes, multi-lobed), local edge optimization, 8-12 diversified restarts."
---

# Point-Based Cluster Strategy for Polygon Optimization

## Why Grid Fails
Grid-based approaches average fish counts over cell areas. A 500x500 cell might have 1 mackerel and 5 sardines, but treating it as "negative score" misses that you could build a thin polygon around just the mackerel. Point-level precision is essential.

## Phase 1: Fish Clustering
- Parse all 2N = 10000 fish positions
- Use spatial hashing (e.g., 100x100 grid of 1000x1000 buckets) to group nearby fish
- For each bucket, compute: mackerel_count, sardine_count, total_count, mackerel_ratio

## Phase 2: Identify Key Clusters
- Mackerel-dense: mackerel_ratio >= 0.6 AND mackerel_count >= 5
- Sardine-dense: sardine_ratio >= 0.7 (regions to avoid)
- Extract the bounding box of each mackerel-dense cluster

## Phase 3: Polygon Construction Strategies
For each mackerel-dense cluster:
- **Strategy A: Minimal Rectangle** - Just the bounding box
- **Strategy B: Expanded Rectangle** - Bounding box expanded by 1-3 units in each direction
- **Strategy C: Merged Rectangle** - If two clusters' expanded boxes overlap, merge them

For combinations of clusters:
- Try L-shapes: combine cluster A (full) + cluster B (partial expansion in one direction)
- Try multi-lobed: connect clusters with thin bridges (only if bridge contains no sardines)

## Phase 4: Score Evaluation and Selection
- For each candidate polygon, compute: mackerels_inside - sardines_inside + 1
- If score < 0, discard
- Track best polygon across all candidates

## Phase 5: Local Optimization
For the best polygon:
- For each edge (up to 100 vertices typically):
  * Try shifts: ±1, ±2, ±3, ±5 units in perpendicular direction
  * Compute new score for each variant
  * Keep shift that improves score
- Repeat 3-5 refinement rounds

## Phase 6: Diversified Restarts
Run 8-12 restarts with different seeds:
- Random subset of top clusters (3-6 clusters per restart)
- Different expansion amounts (1, 2, or 3 units)
- Different merge strategies (aggressive vs conservative)

Output the single best polygon across all restarts.

## C++ Implementation Notes
- Use exact fish coordinates, not grid cells
- Spatial hashing for O(1) cluster lookup
- Efficient point-in-polygon test for axis-aligned polygons
- Limited refinement iterations to stay under 2.0s
- Handle edge cases: no mackerel clusters found, all fish in one cluster, etc.
