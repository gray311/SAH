---
name: discovery-optimization
description: "Optimize orthogonal polygon construction for the NP-hard purse seine fishing problem. Try multiple shape strategies (rectangles, L-shapes, U-shapes), use bounded internal search with greedy refinement, and ensure all 150 test cases complete within time limits."
---

# Orthogonal Polygon Optimization Method

## Task Objective
Maximize (mackerels_in_polygon - sardines_in_polygon + 1) by constructing an axis-aligned orthogonal polygon.

## Step 1: Analyze Input Distribution
- Compute min_x, max_x, min_y, max_y across all points
- Estimate point density in different regions
- Identify sardine-heavy vs mackerel-heavy areas

## Step 2: Try Multiple Construction Strategies

### Strategy A: Bounding Box Rectangle
- Use the extreme points to define a maximal rectangle
- Simple but may include too many sardines

### Strategy B: Shrunk Rectangle
- Start with bounding box
- Iteratively shrink from edges to exclude high-density sardine regions
- Stop when all sardines near edges are excluded or score starts decreasing

### Strategy C: L-Shape Construction
- Find a dense cluster of mackerels
- Build an L-shaped polygon that wraps around them
- Leave out sardine regions that are hard to avoid

### Strategy D: Grid-Based Cell Selection
- Divide the 10^5 x 10^5 space into a coarse grid (e.g., 100x100 cells)
- For each cell, determine if it should be included:
  * Include if mackerel_count > sardine_count + threshold
- Connect selected cells into a valid orthogonal polygon
- This often yields excellent results by local optimization

### Strategy E: Multi-Component Polygon
- Consider allowing multiple disjoint rectangular components
- Each component is an independent axis-aligned rectangle
- Combine them into a single polygon representation

## Step 3: Bounded Search with Greedy Refinement

Implement inside the time limit (target 1.85s max):

1. Generate initial candidate using Strategy D (grid-based) or Strategy B (shrunk rect)
2. Run greedy refinement loop:
   a) Try modifying each edge:
      - Shorten from one end
      - Lengthen until hitting a fish cluster
      - Flip direction if beneficial
   b) Try splitting/merging components
   c) Accept if score improves; otherwise use limited worst-to-best search
3. Keep track of best score found
4. Stop early if score reaches ~5000 (target average)

## Step 4: Validate Output
- Ensure vertex count >= 4
- All vertices distinct
- Total perimeter <= 400,000
- Edges orthogonal
- No self-intersections

## Critical Implementation Notes
- USE THE PROVIDED KD-TREE for O(log N) point-in-rectangle queries
- The evaluator checks ALL 150 test cases — code must be efficient
- Time safety margin: leave 0.1-0.15s buffer
- Output vertices in consistent order (CW or CCW)
- If multiple solutions found, last one scores

## Common Pitfalls
- Don't overcomplicate: a good grid-based heuristic often beats complex geometry
- Don't exceed time limit on simple test cases
- Ensure all constraints are satisfied (validator returns 0 if not)
- Remember: points ON edges count as inside
