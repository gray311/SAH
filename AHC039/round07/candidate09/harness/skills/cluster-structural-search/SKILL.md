---
name: cluster-structural-search
description: Method for constructing polygons using cluster analysis - identify dense mackerel regions, create bite-outs around sardine clusters, and test multiple structural variants.
---

# Cluster-Based Structural Search for Fish Capture

## Overview
This skill guides construction of polygons that strategically capture mackerel clusters
while excluding sardine clusters through bite-out operations.

## Phase 1: Cluster Analysis
1. Build a spatial grid (e.g., 500x500 cells for 0-100000 coordinate range)
2. Count mackerels and sardines in each cell
3. Identify clusters: groups of adjacent cells with high fish density
4. Compute cluster bounding boxes and centers

## Phase 2: Polygon Construction Strategies

### Strategy A: Base Bounding Box
- Compute bounding box of ALL mackerels
- Create simple rectangle: [min_x, max_x] x [min_y, max_y]
- Score: baseline for comparison

### Strategy B: Bite-Out Polygons
For each significant sardine cluster:
1. Start with base polygon
2. Find the edge of base polygon closest to sardine cluster
3. Create an indentation (bite-out) that excludes the sardine cluster
   - Example: if sardines are near the right edge, create a leftward indentation
4. The bite-out adds 2-4 vertices but may reduce mackerel capture slightly
5. Net score = mackerels - sardines + 1; bite-out is worth it if sardines saved > mackerels lost

### Strategy C: Multi-Rectangular Polygons
If mackerels form 2+ distinct clusters:
1. Create separate rectangle for each mackerel cluster
2. Connect rectangles with narrow corridors (1-2 units wide) if needed
3. This captures high-density regions while avoiding sparse (sardine-rich) areas between clusters

### Strategy D: Stepped Polygons
For irregular density distributions:
1. Traverse the density grid from dense to sparse regions
2. Create staircase-like edges following density contours
3. Each "step" adds 2 vertices and better captures irregular shapes

## Phase 3: Variant Comparison
1. Score each candidate polygon (mackerels - sardines + 1)
2. Use probeSolution for quick approximation of variants
3. Select best-scoring valid polygon for full evaluation
4. If all variants score similarly, try different bite-out positions

## Implementation Notes
- Always ensure polygon validity: axis-aligned, no self-intersection, <= 1000 vertices, perimeter <= 400k
- Bite-out depth: typically 100-500 units (adjust based on sardine cluster size)
- Multi-rect connectivity: corridors should be at least 1 unit wide for validity
- Prioritize bite-outs where sardine density significantly exceeds mackerel density
