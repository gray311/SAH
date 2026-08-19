---
name: discovery-optimization
description: "Coordinate-based clustering with rectangle building. Find dense mackerel clusters via coordinate proximity, build bounding boxes, combine into polygons, optimize with edge shifts."
---

# Coordinate-Based Clustering Strategy for Polygon Optimization

## Phase 1: Cluster Analysis
- Read all fish coordinates from input
- Group mackerels by coordinate proximity (use distance-based clustering)
- Find clusters with high mackerel density
- Identify sardine-dense regions to avoid

## Phase 2: Rectangle Construction
For each mackerel cluster:
- Find bounding box: (min_x, min_y, max_x, max_y)
- Count mackerels and sardines inside this rectangle
- Score = mackerels - sardines
- If score > 0, keep this rectangle as candidate

## Phase 3: Combination Strategies
Try these combination approaches:

### Strategy A: Single Best Rectangle
- Pick rectangle with highest mackerels - sardines
- Expand it slightly if improves score

### Strategy B: Rectangle Union
- Combine 2-4 adjacent rectangles
- Merge overlapping areas
- Count fish in union

### Strategy C: L-Shape Construction
- Take two rectangles and form L-shape
- Optimize corner placement

### Strategy D: Complex Polygons
- Build polygon from multiple connected rectangles
- Ensure no self-intersection

## Phase 4: Edge Optimization
For each candidate polygon:
- For each edge, try shifts of ±1, ±2, ±3, ±4, ±5 units
- Use coordinate-based fish counting (not grid approximation)
- Keep shifts that improve score

## Phase 5: Multiple Restarts
- Run 8-12 restarts with different random seeds
- Each restart: pick 3-5 random mackerel points as seeds
- Build clusters around seeds, construct rectangles, optimize
- Track best polygon across all restarts

## Implementation Notes
- Use O(N) fish counting with sorted coordinate arrays
- Use coordinate-based membership testing (point-in-rectangle)
- Avoid grid-based approaches - use exact coordinates
- Limit total operations to stay under 1.9s time limit
- Always output valid polygon format
edit_solution: Replace EVOLVE-BLOCK with C++ implementing coordinate-based clustering:

  1. Read fish coordinates, group by proximity

  2. For each mackerel cluster, build bounding box rectangle

  3. Count mackerels and sardines in each rectangle

  4. Try combinations: single rectangles, unions, L-shapes

  5. Optimize edges with ±1..5 unit shifts

  6. Run 8-12 restarts, output best polygon
evaluate_solution: Run C++ program. Returns score (mackerels-sardines+1), validity, and remaining evaluations (budget=30). Each run has ~1.9s search window.
finish: End when you have encoded coordinate-based clustering with rectangle building and edge optimization.
