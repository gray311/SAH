---
name: discovery-optimization
description: "Fine-grained cluster-based polygon optimization. Build 1000x1000 grid (cell_size=100), find cells with >=3 mackerels, build bounding box polygons, optimize with edge expansion, run 50 trials."
---

# Cluster-Based Polygon Optimization Strategy

## Phase 1: Fine-Grained Grid Analysis
- Use 1000x1000 grid with cell_size=100 (covers 0-100000)
- For each cell, count mackerels only (M)
- Identify clusters: cells with M >= 3
- Sort clusters by M descending, pick top 10

## Phase 2: Bounding Box Construction
For each top cluster:
- Find min_x, max_x, min_y, max_y across all mackerels in cluster
- Create 4-vertex rectangle: (min_x, min_y) -> (max_x, min_y) -> (max_y, max_y) -> (min_x, max_y)
- Verify perimeter <= 400,000 and coords in bounds

## Phase 3: Edge Expansion Optimization
For each rectangle:
- Try expanding each edge by -10, 0, +10 units
- For each expanded rectangle, count M and S inside
- Keep configuration maximizing M - S
- Repeat 2 rounds of optimization

## Phase 4: Multiple Cluster Trials
- Run 50 trials with different cluster selections
- Each trial: pick top 3 clusters, build their bounding boxes, optimize
- Track best polygon across all trials
- Output single best polygon

## Phase 5: Validation
- Ensure 4 <= vertices <= 1000
- Ensure perimeter <= 400,000
- Ensure all coords in [0,100000]
- Output valid polygon

## C++ Implementation Notes
- Use fixed-size 1000x1000 grid for O(1) access
- Pre-compute all cell mackerel counts in O(N) at startup
- Rectangle query = sum of grid cells covering the rectangle
- Total time per evaluation: < 2.0s
- Use efficient grid-based scoring
