---
name: discovery-optimization
description: "Optimize orthogonal polygon construction for NP-hard heuristics. Encloses mackerel clusters while avoiding sardines through iterative probe-based refinement."
---

# Orthogonal Polygon Optimization for Fish Catching Problem

## Objective
Maximize: (mackerels_inside - sardines_inside + 1)

## Strategy
1. Start Simple: Create a 4-vertex rectangle first. Rectangles are perimeter-efficient and easy to position.

2. Find Dense Mackerel Regions: 
   - Look for clusters of mackerel coordinates.
   - Compute bounding boxes of dense regions.
   - These regions are your targets for enclosure.

3. Probe Before You Eval:
   - Use probe_solution to test multiple rectangle positions/sizes.
   - Compare probe scores to find promising regions.
   - Only call evaluate_solution ONCE per major refinement iteration.

4. Refine by Exclusion:
   - Once you have a good polygon, check sardine positions near its boundary.
   - Try notch operations: create L-shaped cuts to exclude sardines outside the main enclosure.
   - Probe these variants before full evaluation.

5. Perimeter Discipline:
   - Keep perimeter < 400000 (use this as a hard constraint in your code).
   - For coordinate range [0, 100000], a maximum rectangle has perimeter 400000.
   - Prefer polygons closer to the origin or with smaller dimensions.

6. Time Budget Awareness:
   - Your C++ code has a 1.95s time limit.
   - Use vectorization, fast point-in-polygon (ray casting or grid-based), and early termination.
   - Precompute results when possible.

## Code Structure
- Read N, then 2N lines of fish coordinates.
- Separate mackerels (first N) and sardines (next N).
- Implement polygon representation: vector<Point>.
- Implement point_in_polygon (handle edge cases: points on edge count as inside).
- Implement score calculation: sum mackerels inside, subtract sardines inside.
- Search loop: try different polygons, keep best.

## Common Pitfalls
- Creating polygons with too many vertices (inefficient perimeter usage).
- Self-intersecting polygons (invalid).
- Going out of bounds (coordinates must be 0-100000).
- Not checking perimeter constraint (will get invalid result).
- Slow point-in-polygon: use grid hashing or sweep-line for 5000 points.

## Example Initial Polygon
Rectangle from (0,0) to (100000, 100000) encloses everything.
Better option: Find min/max of mackerels and use a slightly larger bounding box.

## Iteration Flow
1. analyze_distribution (optional, use what is available)
2. Create initial rectangle
3. probe_solution - test 3-5 variants
4. evaluate_solution - get exact score on best
5. If score low: adjust rectangle bounds to target denser region
6. probe_solution - test adjusted variants
7. evaluate_solution - confirm improvement
8. Repeat 3-5 times, then finish with best
