---
name: square-targeting-strategy
description: For each mackerel, target a 400x400 square centered at the mackerel. Binary search the square size to find the half-width that maximizes (mackerels_in_square - sardines_in_square). Output the best square as a 4-vertex polygon.
---

# Square-Targeting Strategy for Fish Capture

## Overview

Instead of complex corridor expansion, directly target individual mackerels with geometrically-optimal squares.

## Method

### Step 1: For Each Mackerel, Search Optimal Square Size

For each mackerel at position (cx, cy):

- Consider squares centered at (cx, cy) with half-width h ∈ [0, 250]
- For each h, count:
  - m: number of mackerels in [cx-h, cx+h] × [cy-h, cy+h] (inclusive)
  - s: number of sardines in [cx-h, cx+h] × [cy-h, cy+h] (inclusive)
- Score(h) = m - s + 1
- Find h that maximizes Score(h)

### Step 2: Select Top Squares

- Keep the 3 squares with highest scores
- Tie-break by perimeter (prefer smaller squares)

### Step 3: Build Polygons

For each selected square with center (cx, cy) and half-width h:

- Convert to 4 vertices:
  - v1 = (cx - h, cy - h)
  - v2 = (cx + h, cy + h)
  - v3 = (cx + h, cy - h)
  - v4 = (cx - h, cy + h)

- Clamp h to ensure valid coordinates (in [0, 100000])

### Step 4: Output Best Polygon

- Output the polygon that gives maximum (mackerels - sardines)

## Key Points

- Binary search reduces search from O(250) to O(log 250) ≈ 8 steps
- Use spatial grid for O(1) fish counting per step
- Final polygons are simple 4-vertex axis-aligned squares
- This strategy is much simpler and more focused than corridor expansion
