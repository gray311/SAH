---
name: discovery-optimization
description: "Rectangle-based polygon optimization. Direct geometric clustering of mackerels, construct tight bounding boxes, expand rectangles in 4 directions, try 2-3 rectangle unions, hill climb corners, 25 restarts with coordinate extremes and sub-regions."
---

# Rectangle-Based Polygon Optimization Strategy

## Core Insight
The axis-aligned constraint suggests optimal solutions are rectangles or unions of rectangles.
Avoid grid-based approximations; work directly with fish coordinates.

## Phase 1: Parse and Cluster
- Read all fish coordinates from input
- First N points: mackerels (type=1), next N points: sardines (type=-1)
- Cluster mackerels using distance threshold (e.g., 20000 units)
- For each cluster, compute bounding box (min_x, min_y, max_x, max_y)

## Phase 2: Single Rectangle Candidates
For each cluster bounding box:
- Score = count_mackerels_in_rect - count_sardines_in_rect + 1
- Expand in 4 directions: try extensions of +1000, +2000, +5000, +10000 units
- Each expansion: re-score, keep best if perimeter constraints satisfied

## Phase 3: Multi-Rectangle Unions
- Try combining top 2-3 cluster rectangles
- Compute union polygon (may have 8-12 vertices for 2 adjacent rectangles)
- Use inclusion-exclusion to count fish in union
- Ensure: vertices ≤ 1000, perimeter ≤ 400,000

## Phase 4: Coordinate Extremes Strategy
- Try rectangles defined by global min/max coordinates of mackerels
- Try quadrant splits: split by midpoint_x and midpoint_y, evaluate each quadrant
- Try random sub-regions around cluster centroids

## Phase 5: Corner Hill Climbing
For each candidate rectangle/union:
- For each corner, try shifts: ±500, ±1000, ±2000 units (axis-aligned)
- Count fish in new rectangle(s)
- Keep shifts that improve score
- Repeat 2 refinement rounds

## Phase 6: Multiple Restarts (25 restarts)
Each restart:
- Randomly perturb cluster distance threshold (±2000)
- Randomly select 1-3 clusters to focus on
- Build rectangle candidates from selected clusters
- Apply coordinate extremes and quadrant strategies
- Run hill climbing
- Track best polygon

## Phase 7: Output
- Convert best polygon to vertex list
- Validate: 4 ≤ vertices ≤ 1000, coords in [0,100000], integer, no self-intersection
- Output: m then m lines of "x y" (clockwise or counterclockwise)

## Implementation Notes
- Use O(N) rectangle queries: iterate all fish points, check if inside rect
- For unions: use inclusion-exclusion principle
- Total time: <2s with efficient data structures (vectors, direct iteration)
- Use std::chrono for timing, ensure <1.9s safety margin
