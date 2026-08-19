---
name: bbox-construction
description: Construct axis-aligned bounding boxes around mackerel clusters, then expand via exponential contour growth.
---

# Bounding Box Construction and Exponential Contour Expansion

## Step 1: Grid-Based Clustering
- Build 200x200 grid over [0,100000]x[0,100000] (cell_size=500)
- Count mackerels (M) and sardines (S) per cell
- Cell score = M - S, rank cells

## Step 2: Bounding Box for Each Cluster
For top 30 cells:
- Extract all mackerels in that cell
- If mackerels > 0, compute min_x, max_x, min_y, max_y
- Build rectangle with vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- Check validity: perimeter <= 390000, 4 vertices, coords in [0,100000]

## Step 3: Exponential Contour Expansion
For each rectangle:
- Center = ((min_x+max_x)/2, (min_y+max_y)/2)
- For each direction (N,S,E,W,NE,NW,SE,SW):
  * Check adjacent cell's M-S ratio
  * If M >= S or (M > 0 and S < M + 3):
    - Extend contour by 50..200 units in that direction
    - Track if new cells have similar M-S ratio
  * Stop if perimeter > 390000 or quality drops

## Step 4: Refinement
- For each edge, try 8-direction shifts ±5, ±10, ±15, ±20, ±25, ±30
- Use rect_score_fast for O(1) evaluation
- Keep improvements (delta >= 0.5), repeat 4 rounds

## Step 5: Multi-Restart Optimization
- 35 restarts with perturbed cluster selection
- Track best polygon across all restarts
