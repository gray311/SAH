---
name: discovery-optimization
description: "Point-based cluster exploitation. Parse fish coords directly, find mackerel clusters within 500-radius, build rectangles around clusters with careful vertex placement, systematic vertex refinement, 10-15 restarts, use probe_solution to rank candidates."
---

# Point-Based Cluster Exploitation Strategy

## Phase 1: Direct Coordinate Analysis
- Parse fish coordinates directly from input (O(N), not grid-binned)
- Identify mackerel clusters: use Union-Find or BFS to group mackerels within 500-unit distance
- For each cluster, compute:
  * Bounding box: (min_x, min_y, max_x, max_y)
  * Centroid: ((min_x+max_x)/2, (min_y+max_y)/2)
  * Cluster size (num mackerels)

## Phase 2: Initial Rectangle Construction
For each mackerel cluster:
- Create a rectangle starting from centroid
- Expand in 4 directions to include nearby mackerels
- Target dimensions: width/height ≈ cluster_diameter * 1.5
- Place vertices at integer coordinates (use clustering-aware positions)
- For clusters near boundaries, adjust to stay within [0, 100000]

## Phase 3: Multi-Point Polygon Construction
- If you have multiple clusters, try combining them with connecting corridors
- Use axis-aligned rectangles to separate clusters from sardines
- Ensure vertex coordinates are integers and distinct

## Phase 4: Systematic Vertex Refinement
For each candidate polygon:
- For each vertex (up to 1000):
  * Try shifts: ±1, ±2, ±5, ±10, ±20 in x and y directions
  * For each shift, use probe_solution if available for fast scoring
  * Keep shift that improves (mackerels - sardines)
- Repeat 2-3 refinement rounds with decreasing step sizes

## Phase 5: Multi-Restart Search
- Run 10-15 restarts with different strategies:
  * Random perturb cluster selection (±50 in x,y for cluster boundaries)
  * Vary rectangle expansion factor (1.0x to 2.5x)
  * Combine different clusters in various ways

## Phase 6: Final Selection
- Use probe_solution to rank top 10 candidates
- Run full evaluate_solution on best 2-3
- Output best polygon (max score)

## C++ Implementation Notes
- Use Union-Find for efficient clustering in O(N α(N))
- Rectangle intersection check for sardine avoidance
- Fast point-in-rectangle test for scoring
- Total time: <2.0s with efficient algorithms
- Include self-intersection check for polygon validity
