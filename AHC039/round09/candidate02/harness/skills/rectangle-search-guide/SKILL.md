---
name: rectangle-search-guide
description: Use direct rectangle search with O(1) grid counting to find optimal bounding rectangles.
---

# Rectangle Search Guide

## Core Strategy
Directly search for optimal axis-aligned rectangles using grid-based O(1) counting,
instead of building corridors from individual cells.

## Why This Works
- A single large rectangle can capture many more mackerels than thin corridors
- The perimeter budget (400,000) allows large rectangles covering up to 100,000 x 100,000
- O(1) scoring via prefix sums enables exhaustive search within time limits

## Implementation Steps

1. **Grid Construction**: Build prefix sum grids for mackerels and sardines
   - grid_m[x][y] = count of mackerels in [0,x]x[0,y]
   - grid_s[x][y] = count of sardines in [0,x]x[0,y]

2. **Candidate Generation**: 
   - Extract unique x, y coordinates from mackerel positions
   - Limit to top 200 coordinates per dimension
   - Generate all rectangle combinations

3. **Constraint Filtering**:
   - Perimeter <= 400,000: 2*(w+h) <= 400000 => w+h <= 200000
   - Coordinates in [0, 100000]

4. **Scoring**:
   - For each rectangle: m = grid_m[x2][y2] - grid_m[x1-1][y2] - grid_m[x2][y1-1] + grid_m[x1-1][y1-1]
   - For each rectangle: s = grid_s[x2][y2] - grid_s[x1-1][y2] - grid_s[x2][y1-1] + grid_s[x1-1][y1-1]
   - score = m - s + 1

5. **Local Optimization**:
   - Try boundary adjustments ±1, ±5, ±10
   - Keep improvements that maintain constraints

## Key Advantages
- Exhaustive search guarantees finding optimal rectangle
- O(1) scoring enables testing many candidates
- Simple implementation, easy to debug
