---
name: discovery-optimization
description: "Fish-based cluster packing. Parse individual fish positions, cluster mackerels by proximity,\nbuild rectangles around clusters using KD-tree or fine grid, subtract conflicting sardines,\nuse greedy selection with overlap handling, fine-grained edge refinement (\u00b11..15 units),\nrun 8 diverse strategies, output best polygon."
---

# Fish-Based Cluster Packing Strategy

## Phase 1: Fish Parsing and Preprocessing
- Parse mackerels (first N lines) and sardines (next N lines) from input
- Store as Point arrays: mackerels[N], sardines[N]
- Build KD-tree for O(log N) nearest neighbor queries

## Phase 2: Cluster Detection
For each mackerel:
  - Find all other mackerels within distance 150 (squared distance <= 22500)
  - Union these clusters using BFS/DFS on the proximity graph
  - Each cluster gets a cluster_id

## Phase 3: Rectangle Generation
For each cluster:
  - Compute bounding box: [min_x, max_x] x [min_y, max_y]
  - Expand by delta=20: [min_x-20, max_x+20] x [min_y-20, max_y+20]
  - Count mackerels in expanded bbox (using KD-tree range query)
  - Count sardines in expanded bbox (using KD-tree range query)
  - Score = M_count - S_count
  - If score > 0, add to candidate list

## Phase 4: Greedy Selection with Overlap Handling
- Sort candidates by score descending
- Initialize selected_rects = []
- For each candidate (sorted):
  - Check overlap with already selected rectangles
  - If no overlap: select this rectangle
  - If partial overlap: 
    * Try splitting the candidate rectangle to remove overlap
    * Or merge with overlapping rectangle if beneficial
  - Track total score of selected set

## Phase 5: Merge Adjacent Rectangles
- After initial selection, check adjacent rectangles
- If two rectangles share an edge and combined score > sum of individual scores,
  merge them into a larger rectangle

## Phase 6: Fine-Grained Edge Refinement
For each selected rectangle:
  - For each edge (x_min, x_max, y_min, y_max):
    * Try shifts: ±1, ±3, ±5, ±10, ±15 units (NOT coarse ±5..25)
    * Compute new rectangle bounds
    * Count mackerels and sardines using exact point queries
    * If score improves, update the edge position
  - Repeat 2 refinement rounds

## Phase 7: Gap Filling
- Find regions between selected rectangles with high mackerel density
- Try to add small rectangles in these gaps if score improves

## Phase 8: Multiple Strategies
Implement 8 different approaches:
  1. Largest cluster first
  2. Densest region first
  3. Random seed + local search
  4. Greedy by area
  5. Greedy by density (M/S ratio)
  6. Row-wise scanning (scan horizontal strips)
  7. Column-wise scanning (scan vertical strips)
  8. Multi-scale: try different expansion deltas (10, 20, 30)

Output the rectangle configuration with highest score from all 8 strategies.

## C++ Implementation Notes
- Use std::set<Point> for O(log N) point lookup if needed
- Use KD-tree for O(log N) range queries
- Or use 2D grid with cell_size=50 for O(1) queries
- Total time per evaluation: < 2.0s with N=5000 fish
- Edge refinement: 4 edges * 5 shifts * 2 rounds = 40 evaluations max per rectangle
- Use fast bit manipulation or precomputed tables for speed
