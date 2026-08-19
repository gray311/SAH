---
name: discovery-optimization
description: "Fine-grained grid analysis with polygon template exploration. Generate rectangles, L-shapes, U-shapes from mackerel-dense cells, connect with minimal corridors, targeted hill climbing with \u00b11 to \u00b15 shifts, 20-25 restarts."
---

# Refined Polygon Optimization for Axis-Aligned Fish Capture

## Phase 1: Fast Data Loading and Preprocessing
- Read N mackerels and N sardines (N=5000 each)
- Separate into two arrays: mackerels[], sardines[]
- Sort both by x-coordinate for spatial indexing
- Build hash set for O(1) point existence check

## Phase 2: Fine-Grained Grid Analysis
- Use 200x200 grid with cell_size=500 (covers 0-100000)
- For each cell (row, col):
  - Count mackerels M and sardines S inside the cell
  - Compute quality = M - S
  - Store as grid[row][col] = {m: M, s: S, quality: M-S}
- Identify candidate cells: quality > 0 (mackerel-dense)

## Phase 3: Polygon Template Generation
### Template A: Single Rectangle
- Pick one high-quality candidate cell
- Try all combinations of width W and height H from [2, 4, 6, 8, 10, 15, 20, 25, 30, 50]
- Rectangle centered on cell: extends W/2 left/right, H/2 up/down
- Convert to 4 vertices

### Template B: L-Shape
- Pick two adjacent candidate cells (share an edge)
- Form L-shape: combine their bounding boxes with minimal connector
- Try arm lengths [2, 4, 6, 8, 10, 15, 20] for each arm
- Result: 6-8 vertices typically

### Template C: U-Shape
- Pick three candidate cells forming an L-configuration
- Form U-shape enclosing the corner
- Try varying opening widths and arm lengths

### Template D: Multi-Component
- Pick 2-5 candidate cells that are reachable via good paths
- Connect with 1-unit corridors (only through cells where M >= S)
- Form outer boundary

## Phase 4: Local Hill Climbing (Targeted)
For each candidate polygon:
- For each edge (up to 1000):
  - Try expanding outward by +1, +2, +3, +4, +5 units
  - Try shrinking inward by -1, -2, -3 units
  - For each candidate:
    * Count fish inside in O(N) time
    * Update best if score improves
- Repeat 2 refinement passes (use best from pass 1 for pass 2)
- Track best polygon across all attempts

## Phase 5: Multiple Restarts
- Run 20-25 restarts with different random seeds
- Each restart:
  * Randomly perturb candidate cell selection (±5% perturbation)
  * Try 2-3 different template types
  * Run hill climbing
- Output single best polygon found

## Implementation Notes
- Use efficient O(N) scoring per polygon (no re-counting fish)
- Pre-filter candidate cells to reduce search space
- Use integer coordinates only (vertices at integers)
- Validate: 4 <= vertices <= 1000, perimeter <= 400,000
- No self-intersection: consecutive edges meet at vertices only
