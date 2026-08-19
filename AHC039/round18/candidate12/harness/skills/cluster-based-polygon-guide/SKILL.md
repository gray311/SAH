---
name: cluster-based-polygon-guide
description: Use point-based clustering to identify mackerel-dense regions. Build bounding boxes around clusters, avoid sardine-dense regions, merge overlapping boxes, try diverse shapes (rectangles, L-shapes, multi-lobed), local optimization, diversified restarts.
---

# Cluster-Based Polygon Construction Guide

## Core Principle
Fish are at precise coordinates, not distributed in grid cells. Use point-level precision to cluster nearby fish and build polygons around mackerel-dense clusters while avoiding sardine-dense regions.

## Step 1: Spatial Clustering
- Parse all fish positions from input (N mackerels, N sardines)
- Use 100x100 spatial hash (each bucket 1000x1000 units)
- For each bucket: count mackerels, count sardines, compute mackerel_ratio

## Step 2: Identify Dense Clusters
- Mackerel-dense: mackerel_ratio >= 0.6 AND mackerel_count >= 5
- Sardine-dense: sardine_ratio >= 0.7 (regions to avoid or minimize inclusion)

## Step 3: Build Polygon Candidates
For each mackerel-dense cluster:

Option A: Minimal Rectangle
- Compute axis-aligned bounding box of cluster points
- This is your baseline polygon (4 vertices)

Option B: Expanded Rectangle  
- Expand bounding box by 1-3 units in each cardinal direction
- Test each expansion level (1, 2, 3) separately
- Choose the expansion that maximizes score

Option C: Merge with Neighbors
- If cluster A and cluster B are close, compute merged bounding box
- Only merge if merged_score > individual_scores_sum - penalty

For cluster combinations:
- L-shapes: Take cluster A's full box + cluster B's partial expansion in one direction
- Multi-lobed: Connect 3-4 clusters with thin bridges (only if bridge avoids sardines)

## Step 4: Score and Select
- For each candidate, compute: mackerels_inside - sardines_inside + 1
- Discard negative scores
- Track best across all candidates

## Step 5: Local Optimization
- For best polygon, try edge shifts: ±1, ±2, ±3, ±5 units
- Accept shifts that improve score
- Repeat 3-5 refinement rounds

## Step 6: Diversified Restarts
- Run 8-12 restarts with different strategies:
  * Different cluster subsets (3-6 clusters)
  * Different expansion amounts (1 vs 2 vs 3 units)
  * Different merge thresholds

Output single best polygon.

## Key Advantages Over Grid Approach
- Point-level precision: can target individual fish
- Cluster awareness: builds around actual fish distributions
- Flexible shapes: not restricted to corridors
- Better score: typically 20-40% higher than grid-based approaches
