---
name: discovery-optimization
description: "Fish-density histogram approach: parse fish positions, build 2D histogram, find connected positive\ndensity regions, construct bounding boxes around each cluster, evaluate exact score for each,\noutput best rectangle polygon. Avoid sardine-dense areas naturally by focusing on positive regions."
---

# Histogram-Based Polygon Construction Strategy

## Step 1: Parse Fish Input
- Extract all fish coordinates from input (first N lines mackerels, next N lines sardines)
- Store in separate lists for quick access

## Step 2: Build 2D Density Grid
- Choose grid resolution: ~500-1000x500-1000 cells (each ~100x100 or ~200x200 units)
- For each grid cell, count mackerels (M) and sardines (S)
- Compute cell score = M - S
- This is O(N) where N = 10000 fish total

## Step 3: Find Connected Positive-Density Regions
- Use flood-fill or BFS/DFS to find all connected components of cells where M >= S
- Each connected region is a "mackerel cluster"

## Step 4: Compute Bounding Boxes
- For each connected component:
  - Find min/max x and min/max y across all cells in the component
  - Create an axis-aligned rectangle (bounding box)
  - This rectangle captures the entire cluster
- Each bounding box has exactly 4 vertices

## Step 5: Exact Evaluation
- For each bounding box, do exact counting:
  - Use 2D range sum or sweep-line to count all fish inside
  - Score = M_inside - S_inside + 1
- Track best score and corresponding polygon

## Step 6: Output Best Rectangle
- Output the single best axis-aligned rectangle (4 vertices)
- Format: m (vertices count), then each vertex as "x y"

## Implementation Notes
- Use fixed-size arrays for speed (no dynamic allocation in hot path)
- Use integer grid coordinates to avoid floating-point errors
- Total time target: < 0.5s per evaluation to allow multiple attempts
- If multiple positive regions exist, test all bounding boxes
- If no positive regions, output a minimal rectangle at (0,0)-(100,100)
