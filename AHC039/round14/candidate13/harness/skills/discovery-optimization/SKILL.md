---
name: discovery-optimization
description: "Cluster-based rectangle construction with local sardine exclusion. Group mackerels into clusters, build bounding boxes, adjust corners to exclude sardines, merge adjacent rectangles, deep local search with \u00b13..\u00b130 perturbations, 25-30 restarts."
---

# Sardine-Aware Corridor Expansion Strategy

## Phase 1: Grid Construction and Analysis
- Use 200x200 grid with cell_size=500 (covers 0-100000)
- For each cell, count mackerels and sardines from input
- Compute cell score = M - S
- Identify top 15 cells with positive score

## Phase 2: Corridor Expansion (Innovation)
For each top cell, expand in 4 cardinal directions:
- Start from the cell and move outward in one direction
- At each step, check if the new cell has good M-S ratio (M >= S or S < M + 2)
- Stop if: grid boundary, cell score < 0, or sardine density too high (S > M + 2)
- Record the corridor path (sequence of cells)

## Phase 3: Polygon Construction
- Convert corridor sequences into axis-aligned polygon vertices
- For a single direction corridor: create a long thin rectangle
- For multiple directions: combine into an L-shape or multi-lobed structure
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
- Use KVH validator to ensure no self-intersection

## Phase 4: Deep Hill Climbing
For each candidate polygon:
- For each edge (up to 1000):
  * Try shifts: ±5, ±10, ±15, ±20, ±25 units
  * Use grid-based rectangle query for fast scoring
  * Keep shift that maximizes M - S
- Repeat 3 refinement rounds
- Output refined polygon

## Phase 5: Multiple Random Restarts
- Run 15-20 restarts with different random seeds
- Each restart: 
  * Randomly perturb top cell selection (add/subtract random offset to coordinates)
  * Pick 3-5 perturbed top cells
  * Build corridors from each
  * Combine and hill climb
- Track best polygon across all restarts
- Output single best polygon

## C++ Implementation Notes
- Use fixed-size 200x200 grid array for O(1) access
- Pre-compute all cell scores in O(N) at startup
- Rectangle query = sum of grid cells covering the rectangle
- Total time per evaluation: < 2.0s with efficient operations
- Use std::random_device for seed generation
- Include KVH polygon self-intersection check
