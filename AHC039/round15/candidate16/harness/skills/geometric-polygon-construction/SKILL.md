---
name: geometric-polygon-construction
description: Construct axis-aligned polygons from mackerel clusters using coordinate-based rectangle merging and local edge refinement.
---

# Geometric Polygon Construction for Fish Capture

## Core Approach: Coordinate-Based Rectangle Merging

Instead of grid abstraction, work directly with fish coordinates to build precise axis-aligned polygons.

## Step 1: Coordinate Parsing and Storage

- Parse all mackerel (type=1) and sardine (type=-1) coordinates from input
- Store in sorted vectors: vector<Point> mackerels, vector<Point> sardines
- Each Point has x and y integer coordinates

## Step 2: Cluster Detection via Proximity

- For each mackerel, find all mackerels within distance 5000 units (L2 or L infinity)
- Use Union-Find or BFS to group into connected components (clusters)
- For each cluster, compute tight bounding box:
  * min_x = min(x for x in cluster)
  * max_x = max(x for x in cluster)
  * min_y = min(y for y in cluster)
  * max_y = max(y for y in cluster)

## Step 3: Bounding Box Refinement

For each cluster bounding box:

a. Generate coordinate variations for each edge:
   - Left edge: try min_x - 500, -200, -100, -50, 0, +50, +100, +200, +500
   - Right edge: try max_x + 500, +200, +100, +50, 0, -50, -100, -200, -500
   - Bottom edge: try min_y - 500, -200, -100, -50, 0, +50, +100, +200, +500
   - Top edge: try max_y + 500, +200, +100, +50, 0, -50, -100, -200, -500

b. For each candidate rectangle (ax, ay, bx, by):
   - Count mackerels: those with ax <= x <= bx and ay <= y <= by
   - Count sardines: those with ax <= x <= bx and ay <= y <= by
   - Score = mackerels - sardines + 1

c. Keep rectangle with best score that satisfies constraints

## Step 4: Combinatorial Rectangle Merging

- Sort clusters by their centroid position
- Try merging adjacent clusters (horizontal or vertical proximity)
- For 2-cluster merge: union of bounding boxes = larger rectangle
- For 3-4 cluster merges: compute resulting polygon
  * Option A: Convex hull of all cluster bounding boxes
  * Option B: Custom axis-aligned union (may need non-convex polygon)

For each merged shape:
- Compute vertices (for convex hull: standard algorithm; for custom: trace boundary)
- Count perimeter length
- Count mackerels and sardines inside
- Score = mackerels - sardines + 1

## Step 5: Local Edge Optimization

For promising candidate polygons:

a. For rectangles (4 edges):
   - Vary each edge independently by +/-50, +/-100, +/-200, +/-500 units
   - For each variant, recount fish and compute score
   - Keep best variant

b. For complex polygons (n vertices):
   - Vary each vertex by +/-50, +/-100 units in perpendicular direction
   - Ensure edge alignment (x-axis or y-axis)
   - Recompute score for each variant

c. Repeat until no improvement (1-2 rounds)

## Step 6: Multiple Restarts

- Run 10-15 restarts with different seeds
- Each restart:
  1. Randomly select 2-3 mackerels as seed points
  2. Build bounding box around seeds and nearby mackerels
  3. Refine edges with +/-50, +/-100, +/-200, +/-500 shifts
  4. Try merging with adjacent cluster bounding boxes
  5. Local optimization
  6. Score and track best

## Step 7: Output Validation

- Output format:
  m
  x0 y0
  x1 y1
  ...
  x{m-1} y{m-1}

- Constraints:
  * 4 <= m <= 1000 (number of vertices)
  * Perimeter <= 400,000
  * All coordinates in [0, 100000]
  * Integer coordinates
  * No self-intersection

- For rectangles: 4 vertices at (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- For merged shapes: output simplified polygon ensuring axis-aligned edges

## Key Advantages Over Grid-Based Approach

1. Precision: Works with exact coordinates, not coarse 500-unit cells
2. Efficiency: O(N log N) for sorting, O(1) for rectangle queries after setup
3. Flexibility: Can create complex polygon shapes, not just grid-aligned corridors
4. Better Sardine Avoidance: Precise edge positioning minimizes sardine inclusion
