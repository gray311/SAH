---
name: discovery-optimization
description: "Direct coordinate-based clustering. Parse fish coordinates, find dense mackerel clusters, build tight axis-aligned bounding boxes, check sardine presence, ensemble search with 5-10 strategies, coordinate-space search instead of grid."
---

# Direct Coordinate-Based Clustering Strategy

## Phase 1: Coordinate Parsing and Analysis
- Parse all mackerel and sardine coordinates from input
- Store in arrays for fast access
- Sort by x and y for spatial queries

## Phase 2: Cluster Detection
For each mackerel:
  - Check neighbors within distance threshold (e.g., 5000 units)
  - Mark as clustered if connected to existing cluster
  - Track cluster centers and extents

## Phase 3: Bounding Box Generation
For each cluster:
  - Compute min_x, max_x, min_y, max_y
  - Create axis-aligned rectangle with these corners
  - Add 4 vertices to candidate list

## Phase 4: Sardine Check
For each candidate rectangle:
  - Count sardines strictly inside (not on boundary)
  - Count mackerels inside (including boundary)
  - Compute score = mackerels - sardines + 1
  - If score > 0, keep as candidate

## Phase 5: Ensemble Search
Generate multiple candidate polygons:
1. Individual cluster bounding boxes
2. Union of adjacent cluster boxes
3. Large boxes covering top 10% densest mackerel regions
4. Random axis-aligned rectangles (sample random coordinates, expand to ~500x500)
   - For each, check sardine count, reject if > mackerel count
5. L-shaped polygons combining multiple clusters

For each candidate:
  - Validate: 4-1000 vertices, perimeter <= 400000, coords in [0,100000]
  - Score by actual counting (not approximation)

## Phase 6: Time-Based Search
- Allocate time across strategies:
  * 30%: Cluster-based bounding boxes
  * 25%: Individual box variations (shift corners ±100, ±200)
  * 20%: Large region boxes
  * 15%: Random rectangle sampling
  * 10%: L-shaped and multi-lobed combinations

- For each allocation, generate 3-5 candidates
- Score all, output best

## Phase 7: Final Validation
- Ensure output format: m then m lines of "x y"
- Ensure vertices are distinct
- Ensure polygon is valid (non-self-intersecting)
