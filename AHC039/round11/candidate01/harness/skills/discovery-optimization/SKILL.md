---
name: discovery-optimization
description: "Edge extension and hole-filling for sardine avoidance. Start with mackerel bounding box, extend edges, notch around sardines, refine vertices, multiple restarts."
---

# Edge Extension and Hole-Filling Strategy

## Phase 1: Initial Polygon Construction

- Compute bounding box of all mackerels

- Expand the bounding box by 100-200 units in all directions (to capture edge fish)

- Ensure perimeter ≤ 400,000 and coordinates in [0,100000]

## Phase 2: Edge Extension

For each of the 4 sides of the bounding box:
- Try extending outward by 10, 20, 50, 100, 200 units
- For each extension, compute score change
- Keep extensions that improve (mackerels - sardines)

## Phase 3: Sardine Notching

For each sardine inside the polygon:
- Try creating a small rectangular cutout around it
- Cutout size: 10x10 to 50x50 units
- Ensure cutout doesn't remove mackerels
- Score before/after to decide

## Phase 4: Vertex Refinement

For each vertex (up to 1000):
- Try shifting by ±5, ±10, ±20 in x or y direction
- Keep shifts that improve score

Repeat 3 refinement rounds.

## Phase 5: Multiple Restarts

- Run 10-15 restarts with different initial configurations:
  - Vary bounding box expansion (50-300 units)
  - Randomly select which edges to extend
  - Different corner rounding strategies

- Keep best polygon across all restarts

## Phase 6: Multi-Lobed Structures

- Identify dense mackerel clusters
- Create separate rectangular regions for each cluster
- Connect regions with thin corridors if beneficial
- Or output best single-region polygon

## C++ Implementation Notes

- Use efficient O(N) scoring (don't re-scan all fish for each mutation)
- Pre-compute fish positions once
- Use KD-tree or grid for fast rectangle queries
- Keep code simple and bug-free
- Total time: < 2.0s
