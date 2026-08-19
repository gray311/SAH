---
name: discovery-optimization
description: "Cluster-based polygon construction. Detect mackerel-dense clusters, build multiple shape variants (square, rectangle, diamond), search sizes 10k-30k, local edge refinement, output best of 8-12 candidates."
---

# Cluster-Based Polygon Construction Strategy

## Phase 1: Cluster Detection
- Parse input: first 5000 lines are mackerels, next 5000 are sardines
- Use sliding 5000×5000 window to find local maxima of (mackerel_count - sardine_count)
- Identify clusters with ≥5 net positive fish in 1000×1000 windows

## Phase 2: Shape Generation
For each cluster center (cx, cy):

- SQUARE: vertices at (cx-s, cy), (cx+s, cy), (cx+s, cy+s), (cx-s, cy+s)

- RECTANGLE: try aspect ratios 1:1, 1:2, 2:1, 1:3
  e.g., (cx-w, cy), (cx+w, cy), (cx+w, cy-h), (cx-w, cy+h)

- DIAMOND (8 vertices): rotated square approximated with midpoints
  4 corners: (cx±s, cy), (cx, cy±s)
  4 midpoints: (cx±s/2, cy±s/2)

- MULTI-CLUSTER: for 2-3 nearby clusters, take union bounding box

## Phase 3: Size Search
For each shape template and cluster:
- Try side lengths: 10000, 15000, 20000, 25000, 30000 (clamp to bounds)
- Generate 5-7 polygons per cluster

## Phase 4: Local Refinement
For top 3 candidates:
- Try expanding each edge outward by ±50, ±100, ±150 units
- Only keep shifts that don't violate constraints

## Phase 5: Selection
- Output best polygon (highest score, valid constraints)
- Ensure at least 8 diverse candidates generated
- Time budget: ~1.5s per evaluation

## C++ Implementation Notes
- Use efficient coordinate parsing
- Pre-compute cluster centers from all fish positions
- Implement all 4 shape types
- Size parameterized generation
- Bounds checking: 0 ≤ coord ≤ 100000, perimeter ≤ 400000
