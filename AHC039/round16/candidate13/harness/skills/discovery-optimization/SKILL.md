---
name: discovery-optimization
description: "Iterative polygon improvement with grid-based O(1) scoring. Start from mackerel bounding box, use simulated annealing with vertex/edge mutations, prefix sum grid for fast scoring, local hill climb refinement."
---

# Iterative Polygon Optimization Strategy

## Phase 1: Grid Preprocessing

- Build 200x200 grid (cell_size=500) over [0,100000]x[0,100000]
- Read all fish positions, count M (mackerels) and S (sardines) per cell
- Build 2D prefix sum arrays: prefixM[i][j], prefixS[i][j]
- Rectangle query O(1): sum of M/S in [x1,x2]×[y1,y2]

## Phase 2: Initial Polygon

- Find bounding box of all mackerels: [min_x, max_x] × [min_y, max_y]
- If no mackerels or empty, use default 500x500 square at origin
- Create initial 4-vertex polygon from bounding box
- Validate: integer coords, within bounds, valid axis-aligned polygon

## Phase 3: Simulated Annealing Search

For up to 500 iterations:

a) Mutation candidates (generate 5-10 per iteration):
   - Vertex insertion: pick random edge, add point at random position
   - Vertex deletion: pick vertex with degree > 2, try removing
   - Vertex shift: pick vertex, shift coord by ±50..200 (grid-aligned preferred)
   - Edge extension: pick edge, extend one endpoint outward by 100..500
   - Rectangle merge: combine adjacent parallel edges into larger rect

b) Score evaluation:
   - Use prefix sum grid for O(1) M and S counts
   - Compute score = max(0, M_count - S_count + 1)

c) Acceptance:
   - Always accept if score improves
   - Otherwise accept with probability exp((new - old) / T)
   - T starts at 50, decays by 0.95 per iteration

d) Track and update best polygon

## Phase 4: Local Hill Climb

From best polygon, refine for 50-100 steps:

- For each edge:
  * Try extending outward by d = 50, 100, 150, 200, 250
  * Use grid query to score each
  * Keep best valid extension

- Vertex jitter:
  * For each vertex, try ±10, ±20, ±30 on x and y
  * Accept if improves score

- Remove redundant vertices (collinear consecutive vertices)

## Phase 5: Final Validation

- Check: 4 <= vertices <= 1000
- Check: perimeter <= 400,000
- Check: all coords in [0,100000]
- Check: no self-intersection (axis-aligned polygons are simpler to validate)
- Output single best polygon in required format

## Implementation Notes

- Use fast I/O (cin.tie, ios::sync_with_stdio)
- Prefix sum grid: build once O(N), query O(1)
- Total search: ~1000 mutations × O(1) scoring ≈ fast enough for 2s
- Avoid heavy geometric computations (point-in-polygon, etc.)
- Use integer arithmetic where possible
