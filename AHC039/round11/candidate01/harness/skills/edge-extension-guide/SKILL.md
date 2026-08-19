---
name: edge-extension-guide
description: Simple edge extension and hole-filling strategy for polygon optimization.
---

# Edge Extension and Hole-Filling Guide

## Core Strategy

Start with the bounding box of mackerels, then iteratively improve by:
1. Extending edges to capture more fish
2. Notching out regions containing only sardines
3. Refining vertex positions

## Step-by-Step

### Step 1: Initial Bounding Box

- Find min/max x,y among all mackerels

- Create initial polygon: rectangle from (min_x, min_y) to (max_x, max_y)

- Optionally expand by 50-200 units in each direction

### Step 2: Edge Extension

For each of 4 edges (or more vertices if using multi-lobed):

- Try extending outward by amounts: 10, 20, 50, 100, 200

- For each extension, estimate score change:
  - +1 for each new mackerel captured
  - -1 for each new sardine captured
  - Only keep extensions with positive net gain

- Extend all edges that improve score

### Step 3: Sardine Notching

For each sardine inside the polygon:

- Try creating a rectangular cutout (10x10 to 50x50 units)

- Center the cutout on the sardine

- Score before/after the notch

- Keep notches that reduce sardines without losing mackerels

### Step 4: Vertex Refinement

For each vertex (4 to 1000):

- Try shifting by ±5, ±10, ±20 in x or y direction

- Keep shifts that improve score

- Repeat 3 rounds of refinement

### Step 5: Multiple Restarts

- Run 10-15 restarts with:
  - Different bounding box expansions (50, 100, 150, 200, 250)

- Random selection of edge extensions

- Keep the best polygon across all restarts

### Step 6: Multi-Lobed Polygons (Optional)

- If multiple mackerel clusters exist, create separate rectangles

- Connect with thin corridors if it helps capture more fish

- Or stick with single best rectangle

## Key Points

- Keep perimeter ≤ 400,000

- All coordinates in [0, 100000]

- 4-1000 vertices, axis-aligned edges

- Simpler is better: start with rectangles, not complex polygons
