---
name: discovery-optimization
description: "Cluster-based mackerel optimization. Analyze input to find dense mackerel clusters, build minimal-perimeter polygons around top clusters, avoid sardines, combine clusters if beneficial, local edge optimization."
---

# Cluster-Based Mackerel Optimization Strategy

## Core Insight
The optimal strategy is to find compact clusters of mackerels and build minimal-perimeter
polygons around them, rather than using corridor expansion which creates inefficient shapes.

## Step 1: Cluster Detection
- Parse all mackerel positions from input
- Use a distance threshold of 2000 units to group nearby mackerels into clusters
- For each cluster, count mackerels and compute bounding box

## Step 2: Cluster Scoring
- For each cluster, compute minimum enclosing rectangle (MER)
- Count sardines inside each MER
- Score = mackerels - sardines
- Rank clusters by score

## Step 3: Polygon Construction
- Take top 5-10 clusters by score
- Build polygon as union of their MERs
- If MERs overlap, merge to minimize perimeter
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000

## Step 4: Local Optimization
- For each edge of the polygon:
  * Try shifts ±1, ±2, ±5 units
  * Keep shift that improves (mackerels - sardines)
- Repeat 2 rounds

## Step 5: Multiple Restarts
- Run 10-15 restarts with different cluster combinations
- Track best polygon across all restarts

## C++ Implementation Notes
- Use efficient clustering (e.g., simple distance-based grouping)
- Pre-compute MER for each cluster at startup
- Rectangle intersection/union logic for merging
- Time per evaluation: < 2.0s
