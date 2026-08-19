---
name: discovery-optimization
description: "Restart-based polygon expansion with direct edge growth. Start with minimal rectangles, expand edges by 50-200 units, keep improvements. Run 10-15 restarts."
---

# Restart-Based Polygon Optimization Strategy

## Phase 1: Seed Rectangle Selection
- Try creating minimal rectangles at various positions using grid of candidate top-left corners (every 2000 units)
- For each candidate, create rectangle of initial size (10000 x 10000)
- Pick rectangle with highest (mackerels - sardines)

## Phase 2: Directional Expansion
For each seed rectangle, expand in all 4 directions:
- Try expanding each edge by: 50, 100, 150, 200, 250 units
- Count fish inside after each expansion
- Keep expansion that maximizes (mackerels - sardines)

## Phase 3: Multi-Edge Simultaneous Expansion
- Expand multiple edges simultaneously (e.g., top and bottom both by 100)
- This creates larger polygons capturing more fish

## Phase 4: Local Search Refinement
- Shift each vertex by +10, +20, +30, -10, -20, -30 units in all directions
- Try adding or removing vertices to change shape

## Phase 5: Multiple Restarts
- Run 10-15 restarts with different configurations:
  - Different seed rectangle top-left positions
  - Different initial rectangle sizes
  - Different expansion amounts
- Track best polygon across all restarts
- Output single best polygon

## C++ Implementation Notes
- Use fast fish counting: iterate over all fish and check if inside
- Time per evaluation: < 2.0s
- Use integer math to avoid floating-point issues
