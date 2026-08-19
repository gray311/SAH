---
name: discovery-optimization
description: "Grid-based polygon construction for fish trap optimization. Partition space into cells, evaluate mackerel/sardine ratios, construct minimal polygons covering high-ratio regions."
---

# Grid-Based Polygon Construction for Fish Trap

## Problem
Maximize (mackerels - sardines + 1) using an axis-aligned polygon.

## Algorithm
1. **Spatial Grid**: Divide [0, 100000]×[0, 100000] into G×G cells (e.g., G=100 → 10,000 cells).
2. **Cell Ratios**: For each cell, count mackerels (type=1) and sardines (type=-1). Compute ratio = mackerels/(sardines+1) to avoid division by zero.
3. **Select High-Ratio Cells**: Pick top K cells by ratio (e.g., K=500-1000) or cells with ratio > threshold (e.g., >1.5).
4. **Polygon Construction**: For selected cells:
   - Compute bounding box of each group of adjacent cells.
   - Merge adjacent bounding boxes into larger rectangles.
   - Connect rectangles into a simple polygon (chain them in sorted order by x, then by y).
5. **Validity Check**: Ensure no self-intersection, distinct vertices, perimeter ≤400000, vertex count ≤1000.
6. **Internal Search**: Before final submission, try multiple parameter combinations:
   - Grid sizes: 50×50, 100×100, 200×200
   - K values: 500, 800, 1200
   - Thresholds: 1.0, 1.5, 2.0
   - Selection: top-K vs. ratio > threshold
   - Keep the best score.

## C++ Implementation Tips
- Use a flat 2D array for grid cells (grid[row][col]).
- Use KD-tree or sorted lists for fast fish location lookup.
- For polygon merging: use union-find or BFS on grid adjacency.
- Time budget: finish internal search by T - 0.1s.

## Tool Usage
- `edit_solution`: Change the internal search loop, parameter exploration, or construction logic. Keep CPP_CODE entry intact.
- `evaluate_solution`: Score your polygon. Higher = better.
- `probe_solution`: Try parameter variations quickly without consuming budget.

## Common Pitfalls
- Invalid polygon (self-intersection): check before submission.
- Perimeter violation: shrink polygon if >400000.
- Too many vertices: merge collinear vertices.
- Slow search: avoid O(N²) nested loops over fish.
