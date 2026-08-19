---
name: discovery-optimization
description: "Mackerel cluster approximation via bounding rectangles. Find dense mackerel regions, compute tight bounding boxes, extend edges to capture more mackerels while avoiding sardines, use 2D prefix sums for O(1) rectangle scoring, run 10 restarts with \u00b1100..500 initial perturbations, deep refine top 5-10 with \u00b11..4 shifts."
---

# Mackerel Cluster Rectangle Strategy

## Phase 1: Data Parsing and Clustering
- Parse input: first N mackerels, next N sardines
- Group mackerels into cells (e.g., 2000×2000 grid, cell_size=500)
- Count mackerels per cell, identify top 30 cells

## Phase 2: Region-to-Rectangle Conversion
For each top mackerel cell:
- Find all mackerels in that cell and its 8 neighbors
- Compute bounding box: (min_x, min_y) to (max_x, max_y)
- This bounding box is a candidate polygon (4 vertices)

## Phase 3: Sardine Exclusion Check
For each candidate rectangle:
- Count sardines inside using 2D prefix sum (O(1) query)
- Score = mackerels_inside - sardines_inside
- If score < 0, discard or try shrinking

## Phase 4: Edge Expansion (Key Innovation)
For each candidate rectangle, try expanding each edge:
- For top edge: expand downward by d units (d=1,2,3,4), check new sardine count
- For bottom edge: expand upward by d units
- For left edge: expand rightward by d units  
- For right edge: expand leftward by d units
- Keep expansion that improves score (more mackerels, same or fewer sardines)

## Phase 5: Knifing Sardines Out
For rectangles containing sardines:
- Try pushing a single edge outward to "cut" the rectangle corner off
- This removes sardines at the cost of potentially losing some mackerels
- Net gain if sardines_removed > mackerels_lost

## Phase 6: Rectangle Merging
- If two rectangles are adjacent or nearly adjacent, merge them
- Resulting polygon may have 6-8 vertices
- Compute merged rectangle bounding box and re-score

## Phase 7: Deep Refinement
For top 5-10 candidates:
- For each of 4-8 edges: try shifts ±1, ±2, ±3, ±4 units
- Use 2D prefix sums for instant rectangle scoring
- Keep best variant
- Repeat 2-3 refinement rounds

## Phase 8: Multiple Restarts
- Run 10 restarts with different seeds
- Each restart: randomly perturb top cell selection by ±100 to ±500 units
- Build rectangles from perturbed seeds
- Merge, refine, output best

## Performance Notes
- Use 2D prefix sum array for O(1) fish count in any rectangle
- Build prefix sum once: O(N) preprocessing, O(1) per query
- Total per evaluation: <1.5s with 10 restarts and deep refinement
- Output format: m (vertex count), then m lines of coordinates
