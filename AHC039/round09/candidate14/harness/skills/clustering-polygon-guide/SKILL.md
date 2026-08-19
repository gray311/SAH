---
name: clustering-polygon-guide
description: Cluster mackerels by distance, build bounding boxes, exclude sardines, optimize edges.
---

# Clustering-Polygon Guide

## Step 1: Cluster Mackerels
- Parse mackerel coordinates
- Group into clusters using 5000-unit distance threshold
- Each cluster gets its own bounding box

## Step 2: Build Bounding Boxes
- For each cluster: min_x, min_y, max_x, max_y -> 4-vertex rectangle
- Union overlapping rectangles to reduce vertex count
- Ensure total perimeter <= 400,000

## Step 3: Exclude Sardines
- Count sardines inside polygon
- Carve 5x5 exclusion squares around each sardine
- Re-evaluate score
- Adjust exclusion size if needed

## Step 4: Local Optimization
- Shift each edge by +25, +50, +100 units
- Keep shift that improves score
- Repeat 5 rounds

## Step 5: Random Restarts
- Run 10 restarts with different seeds
- Output best result
