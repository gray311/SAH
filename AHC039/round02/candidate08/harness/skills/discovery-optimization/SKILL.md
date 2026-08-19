---
name: discovery-optimization
description: "Optimize axis-aligned polygon construction. Use grid-line analysis: extract X/Y from mackerels,\nbuild bounded candidates, probe before full eval. Edit EVOLVE-BLOCK with targeted diffs.\nBudget: 20 evals. Strategy: analyze -> construct -> probe -> evaluate -> iterate."
---

# Axis-Aligned Polygon Optimization for Grid-Line Problems

## Problem
- Maximize: (mackerels_in_polygon - sardines_in_polygon + 1)
- Polygon must be axis-aligned (edges parallel to x or y axes)
- Constraints: <=1000 vertices, perimeter <=400000, integer coords 0-100000

## Optimal Approach: Grid-Line Construction

### Phase 1: Extract Grid Lines
- Get all unique x-coordinates from mackerels: unique_x = sorted(set(m.p.x for m in mackerels))
- Get all unique y-coordinates from mackerels: unique_y = sorted(set(m.p.y for m in mackerels))
- Count mackerels per line: mackerels_on_x[x] = count of mackerels with p.x == x
- Count sardines per line: sardines_on_x[x] = count of sardines with p.x == x
- Select grid lines: high mackerel density, low sardine density

### Phase 2: Build Polygon Candidates
- Candidate 1 (baseline): bounding box of all mackerels
  min_x = min(m.p.x), max_x = max(m.p.x), min_y = min(m.p.y), max_y = max(m.p.y)
  Polygon: (min_x, min_y) -> (max_x, min_y) -> (max_x, max_y) -> (min_x, max_y)

- Candidate 2 (L-shape): Union of two rectangles using top-2 densest grid lines
  Uses grid_x[0], grid_x[1], grid_y[0], grid_y[1]
  Creates corner piece capturing dense regions

- Candidate 3 (multi-rectangle): Union of 2-3 small rectangles around dense clusters

- Candidate 4 (trimmed bounding box): Remove empty edges, align to actual fish

### Phase 3: Probe & Evaluate
- For each candidate, call probe_solution() - fast approximate score
- Compare probe scores, pick top 2
- Call evaluate_solution() on top candidates only
- If no improvement, try: top-3 grid lines, different L-shape orientation, add small extensions

### Phase 4: Iterate
- Keep winning grid lines, try variations
- If stuck, try different selection: top-k by mackerel count vs by mackerel-sardine ratio
- Consider asymmetric polygons (not symmetric bounding boxes)

## Code Structure to Edit
The EVOLVE-BLOCK contains the main algorithm. Focus on:
- Functions extracting unique coordinates
- Functions building polygon vertices
- Score computation (count fish in polygon)
- Search loop (time-based, <0.15s per eval)

## Important Constraints
- Perimeter: sum of all edge lengths <= 400000
- Vertices: 4 <= count <= 1000
- No self-intersection
- Integer coordinates
- Time limit: ~0.15s internal search, remainder for evaluation

## Template Functions to Add/Modify
Use std::map to count frequencies, std::sort to get top-k, build bounding box from min/max.

Point-in-polygon: For axis-aligned polygons, a simple check works:
  For each edge (x1,y1)->(x2,y2), check if point p is on left/right/top/bottom side.
  Or use ray casting (cross product method) for general case.

## Probing Strategy
- probe_solution() checks ~2000 fish (first subset), ~10 seconds
- evaluate_solution() checks all 10000 fish, ~1-2 minutes
- Use probe to test 5-10 candidates, then evaluate best 2
- Each full evaluation must improve over previous best

## Iteration Pattern
1. analyze_grid_lines -> extract top-k grid lines
2. build_grid_polygon -> generate 3-5 variants
3. probe_solution -> score all variants
4. Select best 2, evaluate_solution
5. If improved: refine grid selection; if not: try different shape
6. Repeat until budget exhausted or improvement stalls
