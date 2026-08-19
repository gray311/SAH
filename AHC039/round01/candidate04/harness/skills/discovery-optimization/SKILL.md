---
name: discovery-optimization
description: "Optimize C++ code for geometric NP-hard problems with time-based internal search.\nUse edit_solution to mutate EVOLVE-BLOCK, evaluate_solution to score, finish when done."
---

# Time-Based Search for Geometric Optimization

## Core Method: Internal Search Loop

Your program MUST implement a search loop inside main() or main's body.
The evaluator runs your code for up to 2 seconds per test case.

### Step 1: Initialize
- Parse input, build data structures (KD-tree, grid, adjacency lists)
- Start with a baseline polygon (bounding box, rectangle covering all points)
- Record baseline score

### Step 2: Search Loop (runs until time expires)
for iteration = 0; elapsed_time < ACTUAL_TIME_LIMIT; iteration++:
  if iteration % 50 == 0:
    # Periodic local search: try small perturbations
    temp_score = evaluate_current_polygon()
    if temp_score > best_score:
      best_polygon = current_polygon
      best_score = temp_score
  
  # Generate candidate polygon
  candidate = mutate_polygon(current_polygon)
  # Mutations: extend edge by k units, move vertex, add/remove vertex
  
  # Quick check: does candidate fit constraints?
  if not fits_constraints(candidate):
    continue
  
  # Quick heuristic score (don't call full evaluator)
  candidate_score = fast_score(candidate)
  if candidate_score > best_score:
    current_polygon = candidate
    best_score = candidate_score

### Step 3: Termination
- When time expires, output best_score polygon

## Mutation Operators to Implement
1. ExtendEdge: extend a horizontal/vertical edge outward by 500-1000 units
2. MoveVertex: shift one vertex by (100,0), (0,100), or (-100,0)
3. AddVertex: insert a new vertex between two existing ones
4. CollapseEdge: remove a vertex (merge two edges)

## Scoring Heuristic
- For each edge segment, count points on a grid aligned with the segment
- Use KD-tree to quickly count points in regions
- This avoids calling the slow evaluator repeatedly

## Constraints to Enforce
- Vertices: 4-1000, all distinct integer coords in [0, 100000]
- Edges axis-aligned (dx=0 or dy=0)
- Perimeter <= 400000
- No self-intersection

## Time Budget
- Use ACTUAL_TIME_LIMIT_SECONDS from constants (~1.95s safe margin)
- Aim for 80-150 iterations per test case
- Each iteration: O(N) or O(log N) with KD-tree
