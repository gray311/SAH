---
name: discovery-optimization
description: "Local cluster-based polygon construction. Group mackerels into spatial clusters, build tight polygons around each cluster avoiding sardines, combine strategically, run 30-40 restarts with fine coordinate precision."
---

# Local Cluster-Based Polygon Construction Strategy

## Core Idea
Instead of coarse grid-based corridor expansion, focus on building tight polygons around individual mackerel clusters using fine-grained coordinate precision.

## Phase 1: Input Parsing and Clustering
- Read all mackerel (first N) and sardine (next N) coordinates
- Group mackerels into clusters using spatial proximity (e.g., 10,000-unit cells or 5-point proximity)
- For each cluster, compute initial polygon as axis-aligned bounding box

## Phase 2: Local Polygon Construction
For each mackerel cluster:
- Start with bounding box of cluster
- Try expanding each edge outward by 0-500 units to include nearby mackerels
- Try shrinking edges to exclude nearby sardines
- Generate multiple variants per cluster

## Phase 3: Variants and Combinations
- For each cluster, try multiple polygon shapes:
  * Bounding box
  * Bounding box with extended sides
  * Custom L-shapes or U-shapes if beneficial
- Try combining 2-4 small polygons into one valid polygon
- Ensure final polygon constraints: 4-1000 vertices, perimeter <= 400,000

## Phase 4: Scoring and Selection
- For each candidate polygon, count exact fish inside using coordinate geometry
- Score = max(0, mackerels_inside - sardines_inside + 1)
- Keep top variants across all clusters and combinations

## Phase 5: Multi-Start Search
- Run 30-40 restarts with different strategies:
  * Different random cluster selections
  * Different expansion amounts
  * Different combination strategies
- Output single best polygon

## Implementation Notes
- Use exact coordinate arithmetic (no grid approximations)
- Implement efficient point-in-polygon tests for axis-aligned polygons
- Use line-segment intersection tests for self-intersection checking
- Keep C++ code efficient to stay under 2.0s time limit
