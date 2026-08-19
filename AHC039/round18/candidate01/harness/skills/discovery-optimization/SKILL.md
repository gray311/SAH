---
name: discovery-optimization
description: "Grid clustering with bounding boxes and exponential contour expansion."
---

# Grid Clustering with Bounding Boxes and Exponential Contour Expansion

## Phase 1: Grid Clustering and Analysis
- Use 500x500 grid (cell_size=200) over [0,100000]x[0,100000]
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify top 30 cells with score >= 0
- Build KD-tree for fast nearest-neighbor queries

## Phase 2: Bounding Box Construction
For each top cell:
- Collect all mackerels within that cell
- If count > 0, build minimal axis-aligned bounding box containing only those mackerels
- Compute perimeter: 2 * (max_x - min_x + max_y - min_y)
- Check constraints: 4 <= vertices <= 1000, perimeter <= 390000, coords in [0,100000]

## Phase 3: Exponential Contour Expansion
For each bounding box, expand in 8 directions:
- Check adjacent cells for better M-S ratio
- Expand if M >= S or (M > 0 and S < M + 3)
- Track perimeter growth, stop if perimeter > 390000 or growth > 5000 per step
- Use convex hull approximation on expanded contour

## Phase 4: Exponential Refinement
For each polygon (4-40 edges):
- For each edge, try 8-direction shifts: ±5, ±10, ±15, ±20, ±25, ±30
- Use grid-based rectangle query for O(1) scoring
- Keep shifts improving M - S by >= 0.5, break ties with smaller perimeter
- Repeat 4 rounds (compounding)

## Phase 5: Multi-Scale Restarts
- Run 35-35 restarts with seeds = chrono + random_device
- Each restart:
  * Perturb top cell selection by ±1..3 grid cells
  * Build 4-8 bounding boxes
  * Try merging adjacent boxes
  * Exponential refinement
- Output single best polygon

## Implementation Notes
- Pre-compute grid in O(N) time
- Bounding box construction O(N log N) with KD-tree or O(N) with grid
- Total time per evaluation: < 1.8s with 35 restarts
