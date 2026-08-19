---
name: discovery-optimization
description: "Coordinate-space vertex construction. Build polygons from mackerel coordinates using bounding boxes around clusters. Expand/contract edges based on sardine positions (O(1) lookup). Run 10-15 construction strategies, keep best."
---

# Coordinate-Space Polygon Construction Strategy

## Core Philosophy

The optimal polygon should be built FROM the fish positions themselves, not from an abstract grid.
Mackerel coordinates provide natural anchor points; sardine coordinates define exclusion zones.

## Step 1: Parse and Index Fish Positions

- Read all fish from input (first N mackerels, next N sardines)
- Store mackerels in sorted list (by x, then y) for clustering
- Store sardines in unordered_set<pair<int,int>> for O(1) point-in-sardine-test
- Track bounding box of all fish: [min_x, max_x] x [min_y, max_y]

## Step 2: Build Single-Fish Bounding Boxes

For each mackerel at (x, y):
  Create rectangle with vertices:
    (x, y), (x+1, y), (x+1, y+1), (x, y+1)
  This minimal rectangle guarantees the mackerel is inside.
  
## Step 3: Cluster Detection

Group mackerels that are close together (within 50 units in both dimensions):
  - Sort mackerels by x-coordinate
  - Iterate and group consecutive mackerels where |x_i - x_j| <= 50 AND |y_i - y_j| <= 50
  - For each cluster, compute tight bounding box
    min_x = min(x for fish in cluster), max_x = max(x for fish in cluster)
    min_y = min(y for fish in cluster), max_y = max(y for fish in cluster)
  - Create polygon from this bounding box (4 vertices)

## Step 4: Sardine-Aware Refinement

For each candidate polygon:
  - Count sardines inside: iterate all sardines, test if inside polygon
    (for axis-aligned rect: min_x <= s.x <= max_x AND min_y <= s.y <= max_y)
  - Count mackerels inside: iterate all mackerels, same test
  - Compute score = mackerels - sardines + 1
  
  Refinement strategies:
  a) Expand edges outward by 1-10 units if score improves
  b) Contract edges inward by 1-5 units if it excludes sardines without losing mackerels
  c) Shift entire polygon toward mackerel density if beneficial

## Step 5: Multi-Cluster Merging

If two cluster bounding boxes are close (distance <= 30 between them):
  Try merging into one larger polygon
  - Union approach: create bounding box of both clusters
  - Or create multi-lobed shape (may have more vertices, ensure <= 1000)
  - Evaluate merged score

## Step 6: Diversified Search Strategies

Run 10-15 independent strategies:
  Strategy 1: Single fish boxes (no clustering)
  Strategy 2: Clustering with radius=20
  Strategy 3: Clustering with radius=50
  Strategy 4: Cluster + outward expansion by 5
  Strategy 5: Cluster + outward expansion by 10
  Strategy 6: Cluster + inward contraction by 3
  Strategy 7: Merge closest pairs of clusters
  Strategy 8: Focus on mackerel-dense regions (use 2D histogram, bin size=100)
  Strategy 9: Start from origin, expand toward mackerel centroid
  Strategy 10: Random perturbations of cluster centers
  
Track best score and best polygon across all strategies.

## Step 7: Output Best Polygon

- Validate: 4-1000 vertices, perimeter <= 400000, coords in [0, 100000]
- If invalid, fall back to minimal valid polygon
- Output format: first line = vertex count, then one line per vertex "x y"

## Complexity and Performance

- Parsing: O(N) where N=5000
- Clustering: O(N log N) with sorting
- Score evaluation: O(N) per polygon (iterate all fish)
- Total per evaluation: ~15 strategies × O(N) = O(15N) ~ 75,000 operations
- Well within 2.0s time limit

## Key Success Factors

- Direct use of fish coordinates (not grid abstraction)
- O(1) sardine lookup for rapid refinement
- Diversified construction strategies to explore different polygon shapes
- Careful validation to ensure output is always valid
