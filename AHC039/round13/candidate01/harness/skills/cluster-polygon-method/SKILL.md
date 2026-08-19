---
name: cluster-polygon-method
description: Use KD-tree to find dense fish clusters, generate bounding-box polygons around them, probe-screen candidates, fine-tune vertices, run multiple restarts.
---

# Cluster-Based Polygon Method for Fish Capture

## Core Strategy

Instead of grid-based approaches, directly work with fish point clusters using KD-tree.
This leverages the spatial structure of actual fish locations.

## Step 1: KD-Tree Construction

- Parse all 10,000 fish (5000 mackerels, 5000 sardines)
- Build balanced KD-tree on all points
- Each node stores: point, left subtree, right subtree, split axis

## Step 2: Cluster Discovery

For i in 1..10:
    1. Sample random point p from uniform distribution
    2. Find all fish within radius R=5000 of p using KD-tree
    3. Compute cluster score = M - S
    4. Store cluster if score > -5 (even negative clusters may improve)

## Step 3: Polygon Generation

For each cluster with bounding box [x1, x2, y1, y2]:
    Generate candidates:
    - Base rectangle: vertices at (x1,y1), (x2,y1), (x2,y2), (x1,y2)
    - Shifted versions: for dx in [-40, -30, -20, -10, 0, 10, 20, 30, 40]
        shifted box: [max(0, x1+dx), min(100000, x2+dx), ...]
    - Total: ~30 candidates per cluster

## Step 4: Probe Screening

For each candidate:
    - Use probe_solution for approximate score
    - If score > 1.5, keep for fine-tuning
    - Else: discard (likely won't be optimal)

## Step 5: Vertex Fine-Tuning

For each surviving polygon:
    - Extract unique x, y coordinates from vertices
    - For each vertex:
        * Try 9 shifts: -15, -10, -5, 0, 5, 10, 15
        * Score each using probe or KD-tree query
        * Keep best shift
    - Repeat up to 3 refinement rounds

## Step 6: Restarts

- 25 independent runs with different random seeds
- Each run: fresh cluster discovery, generation, screening, tuning
- Track best polygon

## Key Advantages

- O(log N) fish counting via KD-tree
- Focus on actual fish density, not artificial grid cells
- Probe screening avoids expensive full evaluations
- Vertex fine-tuning captures subtle improvements
