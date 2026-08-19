---
name: discovery-optimization
description: "Cluster-aware rectangle packing. Build 50x50 grid, identify top 30 mackerel-dense cells, group into clusters, create minimal bounding rectangles, tune boundaries by \u00b15..50 shifts, merge overlapping rectangles, 25-30 restarts, perimeter optimization."
---

# Cluster-Aware Rectangle Packing Strategy

## Phase 1: Coarse Cluster Identification
- Use 50x50 grid with cell_size=2000 (covers 0-100000)
- Count mackerels (M) and sardines (S) in each cell
- Score each cell: M - S
- Identify top 30 cells with highest positive score
- Group nearby high-score cells (within 3 cells) into candidate clusters

## Phase 2: Minimal Bounding Rectangles
For each cluster:
- Find minimal axis-aligned rectangle containing ALL cells in the cluster
- Rectangle bounds: (min_x, min_y) to (max_x, max_y) from cluster cells
- This guarantees capturing all mackerels in the cluster
- Calculate: M_rect = sum of mackerels in all cluster cells, S_rect = sum of sardines in rectangle
- Score = M_rect - S_rect

## Phase 3: Rectangle Selection and Merging
- Select top 20 rectangles by score
- Check for overlaps: merge overlapping rectangles into single polygon
- For non-overlapping: pick single best rectangle OR output as multi-rectangle polygon (vertices = sum of all rectangle vertices)
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000

## Phase 4: Aggressive Boundary Tuning
For each candidate rectangle:
- For each of 4 sides, try offsets: ±5, ±10, ±15, ±20, ±25, ±30, ±35, ±40, ±45, ±50
- New side = original ± offset (constrained to [0, 100000])
- Use grid-based rectangle query to score each variant
- Keep variant with maximum M - S
- Repeat 2 refinement rounds

## Phase 5: Multiple Random Restarts
- Run 25-30 restarts with different random seeds
- Each restart:
  * Randomly perturb cluster selection (use different random subset of top 30 cells)
  * Different grouping threshold (vary from 2 to 5 cells per cluster)
  * Try different merging strategies
- Track best polygon across all restarts

## Phase 6: Validation
- Verify polygon validity: 4-1000 vertices, integer coordinates in [0,100000]
- Check perimeter <= 400,000
- Ensure no self-intersection (use KVH validator)
- Output in required format: m followed by vertex coordinates

## C++ Implementation Notes
- Use 50x50 fixed-size grid for O(1) access
- Rectangle query = sum grid cells covering rectangle, plus boundary adjustments
- Total time per evaluation: < 2.0s with efficient operations
- Use std::random_device for seed generation
- Include KVH polygon self-intersection check
- Focus on perimeter efficiency: maximize (M-S) per unit perimeter
