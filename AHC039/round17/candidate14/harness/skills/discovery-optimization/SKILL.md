---
name: discovery-optimization
description: "Bounding box clustering for mackerel-rich regions. Parse all fish coordinates, group mackerels by proximity, construct axis-aligned rectangles around clusters, try 4-8 vertex variations to exclude sardines, run 10-15 independent searches."
---

# Bounding Box Clustering Strategy

## Core Idea
Directly parse all mackerel and sardine coordinates. Identify dense mackerel clusters and construct tight axis-aligned bounding boxes (possibly with notches) around them.

## Phase 1: Parse and Cluster
- Read all 2N fish coordinates (first N are mackerels, next N are sardines)
- Group mackerels by coordinate proximity: two mackerels are "close" if max(|x1-x2|, |y1-y2|) <= 500
- Use union-find or simple BFS to identify connected components (clusters)
- Track cluster size (number of mackerels) and bounding box for each

## Phase 2: Polygon Construction
For each cluster:
- Compute bounding box: [min_x, max_x] x [min_y, max_y]
- Create a 4-vertex rectangle from this bounding box

For each cluster and bounding box:
- Try variations:
  * Tight bounding box (4 vertices)
  * Slightly expanded box (+100 units in each direction, up to 8 vertices)
  * Box with "notch" to exclude a nearby sardine (if sardine is close to edge)

## Phase 3: Score and Select
- For each candidate polygon, count mackerels and sardines inside
- Compute score = max(0, mackerels - sardines + 1)
- Track the best polygon across all searches

## Phase 4: Output
- Output the best polygon found
- Format: m (vertices), then m lines of "x y"
- Ensure valid axis-aligned polygon with no self-intersection

## C++ Implementation Notes
- Use std::vector<Point> for fish coordinates
- Implement union-find for clustering
- Point-in-rectangle test: x in [min_x, max_x] and y in [min_y, max_y] (inclusive)
- Run 10-15 searches with different cluster combinations and variations
- Total time must be < 2.0 seconds
