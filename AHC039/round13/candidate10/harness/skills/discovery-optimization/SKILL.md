---
name: discovery-optimization
description: "Geometric rectangle-based optimization. Enumerate axis-aligned rectangles using coordinate grid,\ncombine top non-overlapping rectangles into valid polygons, apply local search refinement,\ngenerate multiple diverse candidates, ensure valid output format within time budget."
---

# Geometric Rectangle Optimization Strategy

## Phase 1: Coordinate Analysis
- Extract all unique x and y coordinates from mackerel and sardine positions
- These define the candidate grid for rectangle boundaries

## Phase 2: Rectangle Generation
- For each pair of (x1, x2) and (y1, y2) from unique coordinates
- Create a candidate axis-aligned rectangle [x1, x2] × [y1, y2]
- Count mackerels inside: sum where x1 <= x_m <= x2 and y1 <= y_m <= y2
- Count sardines inside: sum where x1 <= x_s <= y2 and y1 <= y_s <= y2
- Compute score = mackerels - sardines + 1
- Use KD-tree or hash sets for O(log n) or O(1) point containment queries

## Phase 3: Multi-Rectangle Combination
- Select top K rectangles with best individual scores
- Check for overlaps between rectangles
- Combine non-overlapping rectangles into union polygons
- Convert to vertex representation (each rectangle = 4 vertices, shared edges merged)
- Ensure total perimeter <= 400,000 and vertex count <= 1000

## Phase 4: Local Search Refinement
- For each edge of the combined polygon:
  - If edge is horizontal (y constant): try new x positions ±1, ±2, ±3, ±5
  - If edge is vertical (x constant): try new y positions ±1, ±2, ±3, ±5
  - Use approximate rectangle queries to evaluate nearby rectangles
  - Accept improvements, reject worsening moves (optional: use simulated annealing)
- Run 3-5 refinement passes

## Phase 5: Multiple Diverse Seeds
- Generate 20-30 different candidate solutions:
  * Vary the subset of rectangles selected for combination
  * Try different combination strategies (largest area, highest score, most balanced)
  * Use random perturbations of coordinates within bounds
  * Combine with local search each time

## Phase 6: Validation and Output
- Ensure polygon has 4-1000 vertices
- Ensure all coordinates are integers in [0, 100000]
- Ensure no self-intersection
- Output in exact format: m followed by m lines of "a_i b_i"
- If no valid polygon found, output a minimal valid rectangle

## C++ Implementation Notes
- Use fast I/O (std::ios::sync_with_stdio(false))
- Pre-sort fish coordinates for efficient range queries
- Use std::unordered_set or hash-based structures for O(1) lookups
- Implement KD-tree for spatial queries if needed
- Time limit: 2.0 seconds - prioritize fast rectangle counting
- Memory: avoid storing all rectangles, generate on-the-fly
