---
name: polygon-construction-checklist
description: A checklist for constructing high-scoring orthogonal polygons in mackerel-sardine problems. Follow this method to ensure valid, effective constructions.
---

# Polygon Construction Checklist for Mackerel-Sardine Optimization

## Step 1: Validate Geometry
[ ] Exactly 4+ vertices output
[ ] All consecutive vertices form axis-aligned edges (same x or same y)
[ ] All coordinates are integers in [0, 100000]
[ ] Polygon is closed (last vertex connects to first)
[ ] Perimeter ≤ 400,000

## Step 2: Output Format
Line 1: m (vertex count, 4≤m≤1000)
Lines 2..m+1: "x y" coordinates

## Step 3: Common Strategies
[ ] Bounding rectangle: (min_x,min_y), (max_x,min_y), (max_x,max_y), (min_x,max_y)
[ ] Centered rectangle: use centroid, expand by k*std on each axis
[ ] L-shape: subset of rectangle, e.g., cut off top or right

## Step 4: Validation Before Eval
[ ] Check vertex count ≥ 4
[ ] Check consecutive vertices are axis-aligned
[ ] Estimate perimeter: (max_x-min_x)*2 + (max_y-min_y)*2 ≤ 400000
[ ] Verify all coordinates in [0, 100000]

## Step 5: Debugging Low Score
[ ] Is polygon too small? Expand it
[ ] Is polygon missing mackerels? Check bounds
[ ] Is polygon hitting many sardines? Shrink or reposition
[ ] Is perimeter too large? Reduce dimensions
