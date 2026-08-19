---
name: discovery-optimization
description: "Bounding box with sardine exclusion. Discover mackerel clusters via distance-based grouping, build bounding boxes, carve sardine holes, local edge optimization with +25..100 shifts, 10 random restarts."
---

# Bounding Box with Sardine Exclusion Strategy

## Core Idea
Capture mackerel clusters using minimal-perimeter bounding boxes, then carve out sardine-heavy regions as exclusion holes.

## Phase 1: Cluster Discovery
- Parse all mackerel coordinates from input
- Group mackerels into clusters using 5000-unit distance threshold
- For each cluster, compute centroid and axis-aligned bounding box
- Track: cluster size, box perimeter contribution

## Phase 2: Base Polygon Construction
- For each cluster: create 4-vertex rectangle (min_x, min_y, max_x, max_y)
- Union overlapping boxes: merge adjacent/overlapping rectangles
- Ensure: 4 <= total vertices <= 1000, total perimeter <= 400,000
- All coordinates in [0, 100000]

## Phase 3: Sardine Exclusion
- Count sardines inside candidate polygon
- For each sardine: carve 5x5 exclusion square
- Implementation: subtract exclusion squares by splitting polygon
- Re-calculate score after exclusions
- If perimeter exceeds limit: reduce exclusion size to 3x3

## Phase 4: Local Edge Optimization
- For each edge (up to 1000 vertices):
  * Try shifts: +25, +50, +100 units in perpendicular direction
  * For each shift: recalculate mackerel/sardine counts
  * Keep shift that maximizes (mackerels - sardines)
- Repeat 5 refinement rounds
- Early stop if no improvement after 2 rounds

## Phase 5: Multi-Cluster Combination
- Identify top 3 clusters by mackerel count
- Try combining them into single multi-lobed polygon
- Connect clusters with minimal-width corridors
- Evaluate each combination variant

## Phase 6: Random Restarts
- Run 10 restarts with different random seeds
- Each restart: randomly perturb cluster selection
- Build bounding boxes for selected clusters
- Apply sardine exclusions
- Run local optimization
- Track best result across all restarts

## C++ Implementation Notes
- Use O(N log N) sorting for cluster discovery
- Use grid-based O(1) fish counting for fast evaluation
- Sardine exclusion: use polygon subtraction or boolean operations
- Total time per evaluation: < 2.0 seconds
