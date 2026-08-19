---
name: discovery-optimization
description: "Direct cluster-based polygon construction. Use 1000x1000 grid to find mackerel-dense regions, build bounding boxes around fish clusters, expand by 200 units, deep hill climbing with \u00b150..300 shifts over 5 rounds, 25 restarts with adaptive step sizes, full evaluation after promising moves."
---

# Direct Cluster-Based Polygon Optimization

## Phase 1: Point-Based Clustering

- Read all fish coordinates from input (N mackerels + N sardines)
- Build 100x100 grid with cell_size=1000 (covers 0-100000)
- For each cell, count mackerels (M) and sardines (S)
- Compute cell score = M - S
- Identify top 10 cells with positive score

## Phase 2: Cluster-Based Polygon Construction

For each top cell:
- Get all fish (both mackerels and sardines) in this cell
- Compute bounding box: min_x, max_x, min_y, max_y of ALL fish in cell
- Expand each side by 200 units (to capture neighboring clusters)
- Clip to [0, 100000] bounds
- Convert to 4+ vertex polygon (axis-aligned rectangle or L-shape)

## Phase 3: Deep Hill Climbing (5 rounds)

For each candidate polygon:

Round 1: Try shifts ±50, ±100 for each edge (8 directions per edge)
Round 2: Try shifts ±150, ±200 for each edge  
Round 3: Try shifts ±250, ±300 for each edge
Round 4: Try shifts ±100, ±200, ±300 for each edge
Round 5: Try shifts ±150, ±250, ±300 for each edge

For each shift candidate:
- Create modified polygon
- Validate (vertices 4-1000, perimeter <= 400000, coords in bounds, no self-intersection)
- If valid, call evaluate_solution (costs 1 evaluation)
- Track the shift that gives best score

## Phase 4: Adaptive Acceptance

- Accept improving moves 100% of the time
- Accept non-improving moves 20% of the time (simulated annealing-like)
- This helps escape local optima

## Phase 5: Multiple Restarts (25 total)

For restart i in 1..25:
- Generate random seed: seed = i * 12345 + chrono time
- Perturb top cell selection: randomly select 3-6 cells from top 10+5*i
- For each selected cell, build polygon with random expansion (150-250 units)
- Perform 5 rounds of deep hill climbing with adaptive step sizes

## Phase 6: Output

- Select best polygon across all 25 restarts
- Output in format:
  m
  v1_x v1_y
  v2_x v2_y
  ...
  vm_x vm_y

## Key Success Factors

- Finer 1000x1000 grid provides better spatial resolution than 500
- Larger perturbation steps (±50..300) needed for effective exploration
- 25 restarts ensure diverse exploration of search space
- Full evaluation after promising shifts gives accurate feedback
- Adaptive acceptance (20% for non-improving) escapes local optima
