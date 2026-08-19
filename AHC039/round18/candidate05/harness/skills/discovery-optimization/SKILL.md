---
name: discovery-optimization
description: "Cluster-based polygon optimization using KD-tree scoring. Group mackerels by proximity, build polygons around clusters, use \u00b11..3 integer edge mutations, deep hill climbing (5 rounds), 10 restarts."
---

# Cluster-Based Polygon Optimization

## Core Idea

Instead of grid-based abstraction, directly cluster mackerels by spatial proximity and build polygons around dense regions while avoiding sardines.

## Phase 1: Cluster Identification

- Read all fish coordinates from input (5000 mackerels, 5000 sardines)
- Use a simple spatial clustering algorithm:
  - Sort mackerels by x-coordinate
  - Iterate and group points within 500 units of each other
  - Record cluster centroids and counts

## Phase 2: Polygon Construction

For each cluster (or combination of clusters):
- Compute minimum bounding rectangle (axis-aligned)
- If combining clusters, compute union of rectangles (may create multi-segment polygon)
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]

## Phase 3: KD-Tree Scoring

- Use seed's KD-tree to count mackerels and sardines inside polygon in O(log N) per score
- Score = mackerels_inside - sardines_inside + 1

## Phase 4: Deep Hill Climbing

For each candidate polygon:
- For each edge (up to 1000 vertices):
  * Try shifts: ±1, ±2, ±3 units (integer precision)
  * Use KD-tree to count affected fish (points moving in/out of polygon)
  * Keep shift that maximizes score
- Repeat 5 refinement rounds
- Each round: re-optimize all edges, keep best

## Phase 5: Multiple Restart

- Run 10 restarts with different random seeds
- Each restart:
  * Randomly select 2-4 clusters
  * Build initial polygon from their union
  * Perform deep hill climbing (5 rounds)
  * Track best score

## Implementation Notes

- Preserve seed's KD-tree infrastructure for efficient scoring
- Use seed's timer infrastructure to ensure < 2.0s execution
- Integer-only mutations (±1, ±2, ±3) for precise edge tuning
- Output valid polygon in format: m then m lines of "x y"
