---
name: cluster-optimization-guide
description: Find dense mackerel clusters, build minimal-perimeter polygons around top clusters, avoid sardines, combine clusters if beneficial.
---

# Cluster-Based Mackerel Optimization Guide

## Core Strategy
Find compact clusters of mackerels and build minimal-perimeter polygons around them.
This is more effective than corridor expansion because it focuses on high-density regions.

## Step 1: Cluster Detection
- Parse all mackerel positions from input
- Use distance threshold of 2000 units to group nearby mackerels
- Each cluster should contain multiple mackerels (ideally 10+)

## Step 2: Scoring and Ranking
- For each cluster, compute minimum enclosing rectangle (MER)
- Count sardines inside each MER
- Score = mackerels - sardines
- Rank clusters by score (descending)

## Step 3: Polygon Construction
- Take top 5-10 clusters by score
- Build polygon as union of their MERs
- If MERs overlap significantly, merge to minimize perimeter
- Use convex hull or union algorithm for clean polygon

## Step 4: Local Optimization
- For each edge of the polygon:
  * Try shifts ±1, ±2, ±5 units
  * Count mackerels and sardines inside shifted rectangle
  * Keep shift that improves score without adding sardines
- Repeat 2 refinement rounds

## Step 5: Multiple Restarts
- Run 10-15 restarts with different cluster combinations
- In each restart: use a different subset of top clusters
- Track best polygon across all restarts

## Key Success Factors
- Focus on cluster density, not just raw count
- Minimize perimeter by merging overlapping MERs
- Avoid sardines near mackerel clusters
- Use many restarts to explore different cluster combinations

## C++ Implementation Tips
- Use efficient clustering (O(n^2) is fine for 5000 points with small threshold)
- Pre-compute MER for each cluster
- Rectangle union algorithm to merge overlapping MERs
- Time per evaluation: < 2.0s
