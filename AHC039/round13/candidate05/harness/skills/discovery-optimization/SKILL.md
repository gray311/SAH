---
name: discovery-optimization
description: "Coordinate-compressed rectangle optimization. Build prefix-sum grid from fish positions, enable O(1) rectangle queries, iteratively split/shrink rectangles to maximize mackerel inclusion while excluding sardines, deep hill climb with fine-grained edge shifts, 30-40 restarts."
---

# Coordinate-Compressed Rectangle Optimization

## Phase 1: Coordinate Compression

- Extract all unique x coordinates: X = sorted(set of all fish x)
- Extract all unique y coordinates: Y = sorted(set of all fish y)
- Create grid of size |X|-1 by |Y|-1 where cell (i,j) covers [X[i],X[i+1]] × [Y[j],Y[j+1]]
- For each cell, count exact mackerels (M) and sardines (S) inside
- Build 2D prefix sum array: P[i][j] = sum of all M and S in grid[0..i][0..j]
- Rectangle query: count_rect(x1,y1,x2,y2) = P at transformed coords in O(1)

## Phase 2: Initial Bounding Box

- Start with rectangle [0, 100000] × [0, 100000]
- Score = count_mackerel(bbox) - count_sardine(bbox) + 1
- If score ≤ 0, try shrinking to first quadrant or focus on fish distribution

## Phase 3: Rectangle Splitting and Shrinking

For each rectangle in current solution:

### Shrinking Edges
- For each edge (top, bottom, left, right), try shrinking inward by 1, 2, 3, 4, 5, 10, 20, 30, 40, 50 units
- Use prefix sum for O(1) scoring of new rectangle
- Keep configurations with improved score

### Splitting  
- Consider splitting rectangle vertically at each grid x-boundary
- Consider splitting rectangle horizontally at each grid y-boundary
- If split improves total score (sum of both parts), keep the split

## Phase 4: Merging Rectangles

- Find adjacent rectangles that share an edge
- Try merging them (removing shared boundary from perimeter count)
- If merged perimeter + sardine penalty < separate, merge

## Phase 5: Deep Hill Climbing

For each edge of final configuration:
- Try all integer positions from current -50 to current +50
- Score each using O(1) rectangle query
- Move to best position
- Repeat 3-5 passes until convergence

## Phase 6: Multiple Restarts

- Run 30-40 independent searches
- Each restart:
  * Start from bounding box or random subset of rectangles
  * Random order of split/try operations
  * Different random seeds for tie-breaking
- Output best polygon across all restarts

## Implementation Notes

- Use coordinate compression to minimize grid size (at most 10000 unique coords per axis)
- 2D prefix sum enables true O(1) rectangle counting
- Time complexity: O(N log N) preprocessing + O(k·restarts) search where k is search iterations
- Use fast I/O and efficient data structures
- Include polygon self-intersection validation
