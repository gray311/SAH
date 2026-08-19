---
name: discovery-optimization
description: "Bounding-box refinement with coordinate bisection. Start from mackerel bounding box, split edges at quarter/midpoint/thirds, use KD-tree for fast fish counting, max 50 vertices, 5-8 restarts."
---

# Bounding-Box Refinement Strategy

## Core Principle

Start from a tight mackerel-bounding rectangle and iteratively refine edge positions through coordinate bisection.

## Phase 1: Initial Polygon Construction

1. Parse all N mackerel coordinates from input

2. Compute bounding box:
   - min_x = min(mackerel_x), max_x = max(mackerel_x)
   - min_y = min(mackerel_y), max_y = max(mackerel_y)

3. Create initial 4-vertex polygon (axis-aligned rectangle)

4. Count fish inside using KD-tree (4 point-in-rectangle queries, O(log N) each)

## Phase 2: Edge Bisection Refinement

For up to 10 refinement rounds:

For each edge (in priority: longest to shortest):

- Extract edge coordinates: e.g., top edge from (min_x, max_y) to (max_x, max_y)

- Determine split direction:
  * Horizontal edges (top/bottom): vary x-coordinate of one endpoint
  * Vertical edges (left/right): vary y-coordinate of one endpoint

- Try split points at: 0.25, 0.33, 0.5, 0.67, 0.75 of edge length

- For each split point:
  * Create new polygon with one extra vertex (split the edge)
  * Count fish using KD-tree (still O(log N) per query)
  * Track if score improves

- Apply best split (if any improve score)

- Stop if no splits improve score OR polygon reaches 50 vertices

## Phase 3: Interior Quality Check (Optional)

If time remains and score seems suboptimal:

- Build 100×100 grid over polygon interior
- For each grid cell, count sardines inside polygon boundary
- If any cell has sardines >> mackerels, consider:
  * Removing that region (create hole via extra edges)
  * Contracting bounding box further in that direction

## Phase 4: Multiple Restarts

Run 5-8 restarts with different initializations:

1. Standard bounding box of mackerels
2. Bounding box expanded by +1000 in random direction
3. Bounding box contracted by -500 in random direction (if still valid)
4. Random rectangle within [0, 90000] × [0, 90000]
5-8. Slightly perturbed versions of above

For each: build initial → refine → track best

## Phase 5: Final Output

Output single best polygon across all restarts:
- Vertex count, coordinates
- Ensure valid format

## C++ Implementation Notes

- Use KD-tree for O(log N) point-in-rectangle queries
- Edge bisection creates at most 4 + (refinement_rounds × 4) vertices
- With 10 rounds and 4 edges per round: max ~40 vertices (well under 1000 limit)
- Total time per evaluation: < 1.5s with efficient KD-tree
- Use std::random_device for random restart seeds
- No self-intersection guarantee: axis-aligned polygons built via edge splitting don't self-intersect
