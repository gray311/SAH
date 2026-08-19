---
name: polygon-construction-strategy
description: A playbook for constructing orthogonal polygons that maximize (mackerels - sardines + 1). Use this skill to guide your C++ implementation - start with bounding boxes of mackerel clusters, refine using probe-based evaluation, and apply notch operations to exclude boundary sardines.
---

# Strategy for Orthogonal Polygon Construction

## Phase 1: Identify Target Regions
1. Parse mackerel coordinates from input.
2. Compute 2D histogram (grid cells) of mackerel positions.
3. Find top-5 cells with highest mackerel density.
4. For each dense cell, compute its bounding box.
5. Merge overlapping bounding boxes to get candidate enclosures.

## Phase 2: Build Initial Polygons
1. For each candidate enclosure, build a 4-vertex rectangle.
2. Ensure coordinates are integers and within [0, 100000].
3. Check perimeter constraint: must be <= 400000.
4. For rectangle (x1,y1) to (x2,y2): perimeter = 2*(x2-x1 + y2-y1).

## Phase 3: Probe-Based Selection
1. Use probe_solution to score each initial rectangle.
2. Compare estimated scores (probe is cheap, does not consume budget).
3. Select top-3 rectangles for full evaluation.
4. Call evaluate_solution ONCE on each to get exact scores.

## Phase 4: Sardine Exclusion
1. After getting exact scores, identify sardines near polygon boundary.
2. For each boundary sardine, try notching the polygon:
   - Cut out a small rectangle around the sardine.
   - This adds 2 vertices (2 extra perimeter, but excludes sardine).
3. Use probe_solution to test notched variants.
4. If net gain > perimeter penalty, keep the notch.

## Phase 5: Iterative Refinement
1. With remaining time budget, further optimize:
   - Try shifting polygon slightly to capture more mackerels.
   - Try expanding in directions with few sardines.
   - Always probe before full eval.

## Phase 6: Final Selection
1. Compare all evaluated variants.
2. Check validity (non-self-intersecting, correct output format).
3. Select highest score, output vertices.

## Key C++ Implementation Tips
- Use std::vector<Point> for polygon vertices.
- Point-in-polygon: ray casting algorithm (O(log n) with sorting, or O(n) simple).
- For 5000 points, O(n) per point-in-polygon is acceptable if polygon has few vertices.
- Optimization: Pre-sort fish by position, use grid hashing for O(1) density lookup.
- Safety margin: complete computation in < 1.9 seconds (not all 2.0 seconds).

## Code Structure Template
Read input: N, then 2N points
Separate into mackerels[0..N-1] and sardines[0..N-1]
Build density grid (e.g., 200x200 cells for 100000 range)
Find top dense mackerel regions
Generate candidate rectangles
For each candidate, output vertices in correct format
evaluator will score; you want high score
