---
name: discovery-optimization
description: "Cluster-based rectangle construction. Find mackerel clusters within 200 units, compute bounding boxes, score by (M-S+1)/M ratio, select top 10 clusters, build rectangles, merge or output best single polygon. 15-20 restarts."
---

# Cluster-Based Rectangle Construction Strategy

## Core Idea

Instead of grid-based approximation, directly work with fish coordinates to find dense mackerel clusters and build minimal-perimeter rectangles around them.

## Phase 1: Cluster Detection
- Read all fish coordinates from input (5000 mackerels + 5000 sardines)
- Identify clusters: groups of mackerels where pairwise distance <= 200 units
- Use hierarchical clustering: start with each mackerel as its own cluster, merge clusters within 200 units
- Limit to clusters with >= 3 mackerels to avoid noise

## Phase 2: Bounding Box Computation
- For each cluster, compute minimal axis-aligned bounding box:
  - min_x = minimum x-coordinate in cluster
  - min_y = minimum y-coordinate in cluster
  - max_x = maximum x-coordinate in cluster
  - max_y = maximum y-coordinate in cluster

## Phase 3: Cluster Scoring
- For each bounding box, count mackerels and sardines inside
- Score = (mackerels - sardines + 1) / mackerels * 100
- Select top 10 clusters with highest positive score and mackerel count >= 3

## Phase 4: Rectangle Construction
- Convert each selected cluster into a 4-vertex rectangle
- If rectangles overlap significantly, merge them into a single polygon
- If rectangles are separate, choose the one with highest individual score

## Phase 5: Validation
- Ensure polygon has 4-1000 vertices (rectangles have exactly 4)
- Ensure perimeter <= 400,000 (each edge <= 100,000, so 4*4*100,000 = 1,600,000 max, but we select high-density clusters which will be smaller)
- Ensure all coordinates in [0, 100000]
- Use KVH validator for self-intersection check (trivial for rectangles)

## Phase 6: Multiple Restarts
- Run 15-20 restarts with different:
  - Random perturbations to cluster distance threshold (150-250)
  - Different cluster merging strategies
  - Different selection criteria (top 5 vs top 10)
- Output the best polygon across all restarts

## Key Success Factors
- Direct coordinate analysis is more accurate than grid approximation
- Focus on mackerel density, not arbitrary M-S ratios
- Minimal-perimeter rectangles maximize the score
- Multiple restarts explore diverse cluster configurations
- 15-20 restarts provides sufficient diversity while staying under 2.0s time limit
