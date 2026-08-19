---
name: binning-guide
description: Use coordinate binning for fast rectangle scoring, grow rectangles from high-density bins, extend directionally for L-shapes, union collinear rectangles, hill climb, 8 restarts.
---

# Coordinate-Binning Rectangle Optimization Guide

## Core Idea
Replace complex KD-tree with simple coordinate binning for O(1) score queries. Grow rectangles from high-scoring bins and combine collinear ones for better perimeter efficiency.

## Phase 1: Binning
- Create 400x400 grid over [0,100000]² (cell_size = 250)
- For each fish, increment bin at floor(x/250), floor(y/250)
- Store: bins[row][col] = {mackerels, sardines}
- Compute: bin_score = mackerels - sardines
- Find top 8 bins with positive score

## Phase 2: Rectangle Growth
For each top bin:
- Start from bin center (round coordinates to nearest 250)
- Expand step-by-step: at each step, grow rectangle by 25 or 50 units
- At each size, score = sum of all bins covered by rectangle
- Use inclusion-exclusion or cumulative sums for efficiency
- Track best single rectangle

## Phase 3: Directional Extension
From best rectangle, try extending in one direction:
- North: add row above, keep columns
- South: add row below
- East: add column to right
- West: add column to left
- Continue while: marginal score > 0, perimeter < 400,000
- Creates L-shaped or elongated structures

## Phase 4: Collinear Unions
- Find rectangles that share an edge (adjacent, no overlap)
- Union: merge into single rectangle, reducing perimeter
- Score the union and compare to individual rects
- Try all pairs of high-scoring adjacent rectangles

## Phase 5: Hill Climbing
- For each candidate polygon:
  * For each vertex: try shifts ±10, ±20 in valid direction
  * Score using bin sums (O(1) per query)
  * Repeat 2 rounds
  * Keep best improvement
- Must maintain: no self-intersection, integer coords, valid polygon

## Phase 6: Restarts
- 8 restarts with seeds from:
  * Top 3 bins
  * Four corners of [0,100000]²
  * Best from first restart + random offset ±3000
- Each restart explores: single rects, directional extensions, unions
- Track best polygon across all restarts

## Key Success Factors
- Binning provides O(1) score queries (critical for time limit)
- Rectangle growth explores shapes systematically
- Directional extension captures connected clusters
- Collinear unions reduce perimeter penalty
- Hill climbing fine-tunes vertex positions
- Restarts with diverse seeds avoid local optima
