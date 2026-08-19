---
name: discovery-optimization
description: "Two-phase polygon optimization: Quick geometric anchor extraction (bounding boxes, 2x2 blocks, centroid) followed by pattern generation and hill climbing for each anchor."
---

# Two-Phase Polygon Optimization for Mackerel-Sardine Capture

## Phase 1: Quick Geometric Anchors (O(N), <0.1s)

Compute these anchors from all mackerel positions:

1. **Global Bounding Box**: minX, maxX, minY, maxY of all mackerels
2. **2x2 Block Detection**: Find all 2x2 groups of consecutive mackerels (e.g., mackerels at (x,y), (x+1,y), (x,y+1), (x+1,y+1)). Compute bounding box for each 2x2 block. Keep top 5 by mackerel count.
3. **Centroid**: Average of all mackerel positions
4. **Edge-Filtered Box**: For each edge of global bounding box, check if any sardine is within 200 units. If so, shrink that edge inward by 50 units.

## Phase 2: Pattern Generation per Anchor

For each anchor from Phase 1:

**Pattern A: Tight Bounding Box**
- Use anchor's bounding box
- Output 4 vertices

**Pattern B: Holed Bounding Box**
- Start with Pattern A
- For each sardine within 200 units of any edge:
  - Create an indent by adding 2 vertices that push edge inward 50 units toward the sardine
- Output 6-8 vertices

**Pattern C: Corner-Heavy L-Shape**
- Identify which corner of the bounding box is farthest from nearest sardine
- Create L-shape: keep that corner, cut opposite side with 2 indents
- Output 6 vertices

## Phase 3: Hill Climbing Refinement

For each candidate polygon:
- For each edge (4-8 edges):
  - Try shifting inward by ±1, ±2, ..., ±15 units
  - Use grid query to estimate score change
  - Keep shifts that improve score
- Repeat up to 2 rounds

## Phase 4: Multiple Random Restarts

- Run Phases 1-3 with 3 different random seeds (perturb block detection, random indent positions)
- Track best polygon across all runs
- Output single best polygon

## Implementation Notes

- Use cell grid (cell_size=200) for O(1) rectangle/sardine queries
- Phase 1 must complete in <0.1s before Phase 2 begins
- Total time per evaluation: <1.8s to leave safety margin
