---
name: rectangle-optimization-guide
description: Use grid prefix sums to efficiently score rectangles. Build grid, enumerate rectangles anchored at high M-S cells, tune edges, run restarts. Always ensure valid output.
---

# Rectangle Optimization Guide

## Core Strategy

Use 2D prefix sums over a 200x200 grid to enable O(1) rectangle scoring. This allows rapid exploration of many rectangle candidates during optimization.

## Step 1: Grid Construction

- Create 200x200 grid with cell_size=500
- Count mackerels and sardines in each cell
- Compute 2D prefix sums: P[i][j] = sum of all cells (0,0) to (i,j)

## Step 2: Rectangle Scoring

- Rectangle from (min_x, min_y) to (max_x, max_y) has score:
  score = P[max_y/500][max_x/500] - P[min_y/500-1][max_x/500] - P[max_y/500][min_x/500-1] + P[min_y/500-1][min_x/500-1]

## Step 3: Rectangle Enumeration

- Find cells with highest mackerel-to-sardine ratio
- For each high-ratio cell, try rectangles extending outward
- Enumerate (min_row, max_row, min_col, max_col) combinations

## Step 4: Edge Tuning

- For promising rectangles, try small adjustments to corners (±5, ±10)
- Re-score using prefix sums
- Keep best adjustments

## Step 5: Multiple Restarts

- Run 10-15 restarts with different seeds
- Each: pick random high-M cell, enumerate rectangles, tune
- Output best rectangle found

## Critical Constraints

- Rectangle has exactly 4 vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- Perimeter = 2*(max_x - min_x + max_y - min_y) must be <= 400,000
- All coordinates in [0, 100000]
- Always output valid rectangle - invalid output scores 0 for ALL test cases
