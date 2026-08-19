---
name: simple-polygon-optimizer
description: Use simple axis-aligned polygon with edge expansions and multiple restarts. Focus on expanding good rectangles.
---

# Simple Polygon Optimization for Fish Capture

## Core Strategy
Start with minimal rectangles, expand edges, and use multiple restarts to find optimal polygons.

## Step 1: Grid-Based Seed Selection
- Scan coordinate space at regular intervals (every 2000 units)
- For each position, try creating rectangle of various sizes
- Track which rectangles capture most mackerels relative to sardines

## Step 2: Edge Expansion
For each promising rectangle:
- Expand each edge outward by: 50, 100, 150, 200, 250, 300 units
- After each expansion, count fish inside
- Keep expansion that improves score

## Step 3: Multi-Direction Expansion
- Try expanding opposite edges together (e.g., top and bottom both by 100)
- This creates larger, more efficient polygons

## Step 4: Local Search
- Shift each vertex by +10, +20, +30, -10, -20, -30 units in all directions

## Step 5: Multiple Restarts
- Run 10-15 restarts with different configurations:
  - Different seed positions (perturb by +5000 or -5000 randomly)
  - Different initial rectangle sizes
  - Different expansion strategies
- Output best polygon found

## Validation
- Ensure polygon has 4-1000 vertices
- Ensure perimeter <= 400000
- Ensure all coordinates are integers in [0, 100000]

## Key Success Factors
- Use quick scoring to test many expansion options
- Focus on expanding existing good rectangles
- Run enough restarts to explore diverse starting points
- Keep C++ code simple and efficient
