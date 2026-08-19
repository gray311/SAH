---
name: geometric-search-playbook
description: For axis-aligned polygon optimization with mackerel/sardine scoring - 1. Build grid of fish counts per 100x100 cell 2. Start with bounding box covering all mackerels 3. Iterate - extend edges toward high mackerel / low sardine regions 4. Prune edges that add more sardines than mackerels 5. Stop when perimeter > 400000 or no improvement in 50 iterations
---

# Geometric Search Playbook for Axis-Aligned Polygon Optimization

## Problem Understanding
Maximize: mackerels_inside - sardines_inside + 1
Constraints: axis-aligned edges, 4-1000 vertices, perimeter <= 400000
Coords: integer 0-100000, N=5000 each type

## Algorithm: Grid-Based Greedy Growth

### Phase 1: Preprocessing
1. Read all fish positions
2. Build a grid: divide [0,100000]x[0,100000] into 1000x1000 cells
3. For each cell, count mackerels and sardines inside

### Phase 2: Initial Polygon
Start with minimum viable polygon (rectangle):
- Find min/max x and y of mackerels only
- Create rectangle: (minx,miny) -> (maxx,miny) -> (maxx,maxy) -> (minx,maxy)
- Score this baseline

### Phase 3: Edge Extension Loop
For each edge (4 edges initially):
  For direction outward by 500-1000 units:
    - Check new cells crossed
    - Count added mackerels and sardines
    - If delta > 0: extend this edge by that amount
    - Stop if added sardines >= added mackerels
  Repeat for each of 4 sides
  
### Phase 4: Local Search
While time remains and improvement possible:
  For each vertex:
    Try moving by (+/- 100, 0) or (0, +/- 100)
    If valid (axis-aligned, constraints met) and improves score:
      Make the move
  If no improvement in 50 iterations: break

### Phase 5: Optimization
- Collapse edges: remove vertices that create collinear 3+ points
- Ensure no self-intersection (check edge pairs)
- Verify all constraints before output

## Key Tips
- Use KD-tree for fast point-in-region queries
- Grid enables O(1) cell-based scoring
- Time budget: 80-120 iterations max for 2s test case
- Keep polygon simple: prefer fewer vertices
- Perimeter constraint is tight; don't extend too far
