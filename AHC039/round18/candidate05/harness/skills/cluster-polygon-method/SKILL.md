---
name: cluster-polygon-method
description: Build polygons around mackerel clusters using KD-tree scoring and integer edge mutations.
---

# Cluster-Polygon Method for Polygon Optimization

## Overview

This method builds polygons by clustering nearby mackerels and constructing axis-aligned rectangles around them, then refines with precise integer mutations.

## Step 1: Cluster Mackerels

- Read all mackerel coordinates from input
- Sort by x-coordinate
- Iterate through sorted list, grouping points within 500 units
- Each group forms a potential cluster

## Step 2: Build Initial Polygons

For each cluster:
- Find min/max x and y coordinates
- Create axis-aligned rectangle (4 vertices)
- Score using KD-tree query

For combinations of adjacent clusters:
- Compute union of bounding boxes
- May require 6-8 vertices for L-shaped unions
- Score each combination

## Step 3: KD-Tree Scoring

- Use the existing KD-tree to count points inside polygon
- Iterate through all mackerels and sardines
- For each point, check if inside polygon (ray casting or coordinate check for axis-aligned)
- Score = mackerels_inside - sardines_inside + 1

## Step 4: Deep Hill Climbing

For each polygon candidate:

Round 1-5 (5 rounds total):
- For each edge of the polygon:
    * Try shifting the edge by ±1, ±2, ±3 units
    * Recompute polygon with new edge
    * Score using KD-tree
    * Keep shift that improves score
- After trying all edges, keep the best modified polygon

## Step 5: Multiple Restarts

- Run 10 restarts with different random seeds
- Each restart:
    * Randomly pick 2-4 clusters
    * Build initial polygon from their union
    * Perform 5 rounds of deep hill climbing
    * Track best score

## Key Techniques

- Use integer-only mutations (±1, ±2, ±3) for precise edge tuning
- Leverage KD-tree for O(log N) scoring
- Deep hill climbing (5 rounds) to escape local optima
- Multiple restarts to explore different cluster combinations
