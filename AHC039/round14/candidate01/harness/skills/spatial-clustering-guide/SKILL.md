---
name: spatial-clustering-guide
description: Use spatial clustering (find_fish_clusters) to locate dense mackerel regions, build axis-aligned rectangles, expand with probe-guided search, 10-15 restarts.
---

# Spatial Clustering with Probe-Guided Expansion

## Step 1: Cluster Analysis (CALL ONCE)
- Call find_fish_clusters to build quadtree from all 10,000 fish points
- Get top 50 mackerel clusters (sorted by count)

## Step 2: Base Rectangle Construction
For each of the top mackerel clusters:
- Create initial rectangle with vertices at cluster boundaries
- Ensure 4 vertices, integer coords in [0,100000], perimeter ≤ 400,000

## Step 3: Probe-Guided Expansion
For each base rectangle:
- Use probe_solution to score the current rectangle
- Try expanding in each cardinal direction by 50-1000 units
- Keep expansion with best probe score and perimeter < 400,000

## Step 4: Deep Hill Climbing
For each expanded polygon:
- For each edge: try shifts ±10, ±20, ±30, ±40, ±50 units
- Use probe_solution for each shifted variant
- Keep shift with best probe score
- Repeat 2 refinement rounds

## Step 5: Multiple Restarts
- Run 10-15 restarts with different starting clusters
- Use probe_solution to rank candidates before final evaluate_solution

## Step 6: Final Selection
- Use evaluate_solution ONCE for the best probe-ranked candidate
- Output: m then m lines of "x y"

## Key Points
- find_fish_clusters runs ONCE and informs all subsequent decisions
- probe_solution enables fast iterative refinement (30-probe budget)
- evaluate_solution is expensive; only call with best candidates
