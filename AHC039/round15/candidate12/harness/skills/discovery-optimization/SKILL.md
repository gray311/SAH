---
name: discovery-optimization
description: "Direct point clustering + greedy polygon growth. Build 1000x1000 grid for fast lookup, find mackerel-dense seeds, grow polygons by expanding edges while improving (M-S) score, refine with local edge perturbations \u00b13..8."
---

# Direct Clustering and Greedy Growth Method

## Phase 1: Parsing and Grid Setup
- Read input: N=5000 mackerels, then N=5000 sardines
- Store in std::array or std::vector<Point> for O(1) access
- Build 1000x1000 spatial grid (cell_size=100)
- For each fish, increment M or S count in corresponding cell
- Compute cell_score = M - S for each cell

## Phase 2: Seed Selection
- Find top 8 cells with positive cell_score
- These are our starting locations for polygon construction

## Phase 3: Greedy Polygon Growth
For each seed cell:
- Start with minimal bounding box around fish in that cell (4 vertices)
- Compute exact score for this initial polygon
- Try expanding each of the 4 edges in outward direction:
  * For horizontal edge at y=Y from x=L to x=R:
    - Try new edge at y=Y+Δ for Δ in {+3,+5,+8}
    - Compute score of expanded polygon
    - Keep if score improves
  * Similarly for vertical edges
- Continue expanding until: no improvement, perimeter > 400000, vertices > 1000
- Track best polygon from this seed

## Phase 4: Exact Scoring
- To count fish in polygon: iterate all 10000 fish points
- For axis-aligned polygon: point is inside if it's within the boundary
- Use simple point-in-polygon test (ray casting or sequential edge checks)

## Phase 5: Local Hill Climbing
- For the best polygon from Phase 3:
  * For each vertex, try perturbing x or y by ±3, ±5, ±8
  * Ensure new coordinates in [0,100000]
  * Compute score for perturbed polygon
  * Apply improvement
  * Repeat 2 rounds

## Phase 6: Output Best
- Output vertex count followed by vertices
- Ensure valid format and constraints

## Performance Notes
- Use flat arrays, avoid dynamic allocation
- Pre-allocate buffers for grid, fish storage
- Time-based early exit: if time < 0.25s, output current best
- Target <1.8s per evaluation for safety margin
