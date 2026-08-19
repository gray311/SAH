---
name: discovery-optimization
description: "Direct packing strategy for fish capture polygon. Sort mackerels and sardines, create bounding boxes around clusters, adjust boundaries to exclude sardines, use 5x5 cell clustering for multi-region capture, advanced hill climbing with 8-direction perturbations."
---

# Direct Packing Strategy for Fish Capture

## Phase 1: Fish Data Loading and Pre-processing
- Parse all fish positions from input
- Store mackerels and sardines in separate arrays
- Compute basic statistics (min/max x/y, total counts)

## Phase 2: Cluster-Based Packing
### Option A: K-Way Clustering (Primary Strategy)
1. Divide [0,100000]x[0,100000] into a 5x5 grid (cell_size=20000)
2. For each cell, count mackerels (M) and sardines (S)
3. Select cells where M > S (positive score)
4. For each selected cell:
   - Find the bounding box of mackerels in that cell
   - Create a rectangle that encloses these mackerels
   - Expand the rectangle in all 4 directions as long as:
     * New cells have M > S
     * No sardines are on the boundary
   - Store the rectangle as a candidate
5. Combine all rectangles into a single polygon:
   - Sort rectangles by their centroid
   - Use a greedy approach to merge overlapping rectangles
   - Ensure the final polygon has valid axis-aligned edges

### Option B: K-Way Sorting (Secondary Strategy)
1. Sort all mackerels by x-coordinate
2. Take the top K mackerels (K=500) as the "target cluster"
3. Find the bounding box of these K mackerels
4. For each side of the bounding box:
   - Check if any sardines are on that edge
   - If yes, shift the edge to exclude sardines while still enclosing mackerels
   - Expand the edge outward if it captures more mackerels
5. Output the final polygon

## Phase 3: Sardine-Aware Boundary Adjustment
For each edge of the polygon:
- Check if any sardine lies on this edge (using integer arithmetic)
- If a sardine is on the edge, shift the edge by 1 unit in the direction that excludes it
- Repeat until no sardines are on any edge

## Phase 4: Advanced Hill Climbing
For each vertex of the polygon (up to 1000):
- Try perturbing in 8 directions: N, NE, E, SE, S, SW, W, NW
- For each direction, try 3 distances: 100, 200, 500 units
- Compute the score for each perturbed polygon
- Accept the perturbation that gives the highest score
- Repeat for up to 100 iterations or until no improvement

## Phase 5: Multiple Restarts
- Run 5-10 restarts with different strategies:
  * Vary the clustering grid size (5x5, 10x10, 20x20)
  * Vary the K value for top-K sorting
  * Vary the initial polygon construction method
- Track the best polygon across all restarts
- Output the best polygon

## Implementation Notes
- Use efficient data structures for fish position lookups
- Pre-compute fish positions into arrays for fast access
- Use integer arithmetic for all coordinate calculations
- Ensure the final polygon satisfies all constraints:
  * 4 <= vertices <= 1000
  * Integer coordinates in [0,100000]
  * Perimeter <= 400000
  * No self-intersection
- Limit total execution time to < 2.0 seconds
