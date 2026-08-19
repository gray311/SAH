---
name: discovery-optimization
description: "Cluster-based mackerel aggregation. Use DBSCAN-like clustering on mackerel coordinates, identify pure clusters (no nearby sardines), expand bounding boxes carefully, hill climb with \u00b110..40 shifts, 10-12 restarts."
---

# Cluster-Based Mackerel Aggregation Strategy

## Phase 1: Spatial Clustering
- Use KD-tree or direct spatial indexing for fish positions
- Group mackerels into clusters using distance-based criteria:
  * For each mackerel, count neighbors within radius 200
  * Form clusters of 3+ mackerels with pairwise distance < 300
- Identify cluster centers (centroid or furthest pair midpoint)

## Phase 2: Pure Cluster Detection
- For each cluster, check for nearby sardines:
  * Query sardines within 300-radius of cluster bounding box
  * If 0 sardines found → "pure cluster" (high priority)
  * If 1-2 sardines at boundary → "mixed cluster" (medium priority)
  * If many sardines → skip or handle carefully

## Phase 3: Bounding Box Expansion
- For each pure cluster:
  * Compute tight bounding box (min_x, max_x, min_y, min_y)
  * Add padding: expand by 50-100 units in each direction
  * Snap to integer coordinates
- For mixed clusters with careful boundaries:
  * Compute bounding box, then adjust edges to exclude sardines
  * May result in non-rectangular (multi-edge) polygons

## Phase 4: Polygon Construction
- Convert cluster bounding boxes to axis-aligned polygons
- Can combine adjacent clusters into larger polygons if beneficial
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
- Validate with self-intersection check

## Phase 5: Deep Hill Climbing
For each candidate polygon:
- For each edge (up to 1000 vertices):
  * Try shifts: ±10, ±20, ±30, ±40 units
  * Count actual mackerels and sardines inside (direct geometry, no grid)
  * Keep shift that maximizes (mackerels - sardines)
- Repeat 3 refinement rounds
- Output refined polygon

## Phase 6: Multiple Random Restarts
- Run 10-12 restarts with different seeds
- Each restart: randomly perturb cluster formation, rebuild from scratch
- Track best polygon across all restarts
- Output single best

## Key Differences from Grid-Based Approach
- Works directly with fish coordinates (no 500-unit cell abstraction)
- Uses actual clustering logic instead of coarse grid scoring
- Better at finding small, pure mackerel regions
- More accurate scoring during hill climbing
