---
name: discovery-optimization
description: "Optimize C++ fish-catching polygon code for 150 test cases, 2.0s per case,\nscore = mackerels - sardines + 1. Use task_parameter_analyzer for recommendations.\nEnsure search completes within ~1.95s per case."
---

# Fish Catching Polygon Strategy

## Problem
Maximize: (mackerels in polygon) - (sardines in polygon) + 1
- N = 5000 fish each, rectilinear polygon (up to 1000 vertices)
- Coordinates: integers 0..10^5, 150 test cases, 2.0s limit
- Points on edges count as inside

## Optimal Algorithm: Grid-Based Clustering
1. Divide coordinate space into grid cells (e.g., 100x100)
2. Count mackerels and sardines in each cell
3. Identify cells with positive (mackerels - sardines)
4. Group adjacent positive cells into rectangles
5. Build polygon from these rectangles
6. Try multiple grid resolutions, keep best

## Key Implementation Details
- Use grid hashing (array indexed by cell coordinates) for O(1) lookups
- Pre-allocate arrays to avoid dynamic allocation
- Time-box search to ~1.8s for safety margin

## Data Structure Choice: Grid Hashing
- Array of cells: grid[x//res][y//res][0=mackerels, 1=sardines]
- O(1) cell lookup, O(N) population
- Simple and fast for this problem
