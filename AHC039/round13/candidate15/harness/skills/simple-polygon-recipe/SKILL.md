---
name: simple-polygon-recipe
description: Build simple axis-aligned rectangles or L-shapes around dense mackerel regions. Use minimal hill climbing.
---

# Simple Polygon Construction Recipe

## Core Strategy
Target dense mackerel regions directly, build simple polygons (rectangles, L-shapes), minimal refinement.

## Step 1: Grid-Based Density Estimation
- Divide [0,100000]² into grid (e.g., 50x50 cells)
- Count mackerels and sardines per cell
- Score = M - S

## Step 2: Identify Seed Regions
- Select top 5-10 cells with highest positive (M-S) score
- These are your target regions

## Step 3: Build Simple Polygons
For each seed cell at (cx, cy):

**Rectangle option:**
- Expand equal distance d in all 4 directions
- Vertices: (cx-d, cy-d), (cx+d, cy-d), (cx+d, cy+d), (cx-d, cy+d)

**L-shape option:**
- From corner, expand 2+ directions
- e.g., expand East and North to form L-shape

## Step 4: Minimal Hill Climbing
- For each edge vertex, try shifts: -3, -2, -1, +1, +2, +3
- Score each variant (use probe for speed)
- Keep improving shift
- Repeat 1-2 rounds

## Step 5: Output Best Polygon
- Validate: 4-1000 vertices, perimeter ≤ 400,000, coords in [0,100000]
- Ensure axis-aligned (edges parallel to x or y axis)
