---
name: geometric-cluster-union-guide
description: Use geometric clustering to group mackerels into proximity clusters, compute bounding boxes, union them into polygons.
---

# Geometric Cluster Union Guide

## Core Principle
Group nearby mackerels into clusters, then create a polygon that is the union of bounding boxes around each cluster.

## Step 1: Distance-Based Clustering
- Use Manhattan distance threshold (typically 2000 units)
- Group mackerels into clusters using BFS/Union-Find
- Each cluster contains all mackerels within threshold distance

## Step 2: Compute Bounding Boxes
- For each cluster:
  * min_x = minimum x coordinate
  * max_x = maximum x coordinate
  * min_y = minimum y coordinate
  * max_y = maximum y coordinate
  * mackerel_count = number of mackerels in cluster
- Count sardines inside each bounding box

## Step 3: Score Clusters
- score = mackerel_count - sardine_count
- Sort clusters by score descending
- Consider: should we use all clusters or top k?

## Step 4: Union Clusters into Polygon
- Sort clusters by x coordinate
- Merge adjacent/overlapping clusters to minimize perimeter
- Build stepped polygon by connecting bounding boxes
- Ensure: 4-1000 vertices, valid polygon (no self-intersection)

## Step 5: Sardine Exclusion
- Check if sardines lie on edges or inside polygon
- Try expanding boxes slightly (1-5 units) if safe
- Use KD-tree for fast containment queries

## Step 6: Multiple Strategies
- Try different distance thresholds (1500, 2000, 2500, 3000)
- Try using top k clusters (k=5, 10, 15, all)
- Output best polygon across all strategies

## Implementation Notes
- N=5000 mackerels, 2.0s time limit
- Use BFS clustering: O(N * N) worst case but typically fast
- Bounding box sardine count: O(N * num_clusters)
- Total should fit in time budget
