---
name: discovery-optimization
description: "Exact 2D prefix sum for O(1) rectangle scoring. Sample random rectangles, optimize corners locally, combine if beneficial, 30 restarts."
---

# Exact 2D Prefix Sum Polygon Optimization

## Core Innovation: 2D Integral Image

Replace grid-based approximation with EXACT 2D prefix sums for O(1) rectangle queries.

## Step 1: Build Prefix Sum Array

- Create 2D array prefix[x][y] where prefix[x][y] = sum of all fish (mackerels +1, sardines -1)
  in rectangle [0,0] to [x,y]
- Use standard 2D prefix sum formula:
  prefix[x][y] = fish[x][y] + prefix[x-1][y] + prefix[x][y-1] - prefix[x-1][y-1]
- Initialize with 0s, build in O(W*H) where W,H = 100000

## Step 2: Query Rectangle Score

- Rectangle [(x1,y1), (x2,y2)] score = prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]
- O(1) query time

## Step 3: Rectangle Sampling

- Generate 1000 random pairs of corners from [0, 100000]x[0, 100000]
- For each pair, compute rectangle score using prefix sums
- Filter: score > 0, perimeter = 2*(w+h) <= 400,000, area > 0

## Step 4: Local Corner Optimization

- For each candidate rectangle, try perturbing each corner by ±5, ±10, ±15, ±20
- Keep perturbations that improve score
- Repeat 3 refinement rounds

## Step 5: Multi-Rectangle (Optional)

- Try combining 2-3 non-overlapping rectangles
- Ensure total perimeter constraint satisfied
- Usually single large rectangle is best

## Step 6: Multiple Restarts

- 30 restarts with different random seeds
- Each restart independent: build prefix, sample, optimize
- Track best polygon across all restarts

## Step 7: Output

- Single rectangle: output 4 vertices in order
- Multiple rectangles: output vertices of each, total vertices <= 1000
- Perimeter <= 400,000, all coords in [0, 100000]
