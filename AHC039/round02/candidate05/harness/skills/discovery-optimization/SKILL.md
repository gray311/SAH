---
name: discovery-optimization
description: "Optimize polygon-finding C++ code for NP-hard heuristic tasks. Build bounded internal search loops that construct multiple orthogonal polygons, validate them efficiently, and output the best one within time limits. Use validate_polygon to screen variants before expensive evaluations."
---

# Orthogonal Polygon Optimization Strategy

## Objective
Maximize: (mackerels_inside - sardines_inside + 1) using an orthogonal polygon.

## 4-Phase Search Loop (inside C++ main loop)

### Phase 1: Setup
- Read all fish coordinates into arrays
- Build spatial index (grid or KD-tree) for fast point queries
- Store fish in separate lists: mackerels (type=1), sardines (type=-1)

### Phase 2: Construct Multiple Polygons
Implement 3+ construction strategies:

Strategy A: Grid-Sweep from Centroid
- Find bounding box of all mackerels
- Start from centroid or a chosen mackerel
- Grow 4 directions (N,S,E,W) placing vertices on integer grid
- Each segment must be axis-aligned and <= 200000
- Prefer vertices that include mackerels, avoid sardines

Strategy B: Rectangle Expansion
- Start with smallest rectangle containing all mackerels
- If perimeter > 400000, shrink or merge with neighbor rectangles
- Iteratively add pockets that include mackerels but exclude sardines

Strategy C: Perimeter-Constrained Path Following
- Sort mackerels by x-coordinate
- Build orthogonal path visiting ~200-500 mackerels
- Close the loop ensuring orthogonality and perimeter <= 400000

For each construct:
1. Call validate_polygon to check constraints
2. If invalid, discard and try different parameters
3. If valid, store for potential evaluation

### Phase 3: Evaluate Top Candidates
- Use probe_solution if available to rank top 5-10 polygons cheaply
- Evaluate only the top 3-5 using evaluate_solution
- Track best score

### Phase 4: Output
- Output the polygon with highest combined_score
- Format: vertex_count, then x0 y0, x1 y1, ..., x_{n-1} y_{n-1}

## Implementation Notes
- Time budget: ~1.85s for search + evaluation
- Aim for 10-20 full evaluations with good pre-ranking
- Use long long for perimeter calculations
- Free all dynamic memory before exit

## Failure Recovery
- If validation fails: check if vertex count > 1000 or perimeter > 400000
- If timeout: reduce number of constructs or evaluation candidates
- If all polygons invalid: fall back to simple 4-vertex rectangle covering all mackerels
