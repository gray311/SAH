---
name: discovery-optimization
description: "Multi-strategy geometric search: direct coordinate analysis, cluster bounding boxes, \nmulti-rectangle unions, ridge following, dense region expansion, randomized exploration. \nAggressive local search with \u00b1150..600 shifts. 5+ construction strategies per eval."
---

# Multi-Strategy Polygon Construction

## Core Insight

The previous coarse grid (500-unit cells) failed to capture local density variations.
Use direct coordinate analysis with 1000-unit cells and multiple construction strategies.

## Phase 1: Spatial Index Setup

- Parse all fish coordinates into arrays
- Build hash map: (x, y) -> fish type for O(1) lookups
- Build 1000x1000 grid cells, each storing (mackerel_count, sardine_count)

## Phase 2: Five Construction Strategies

### Strategy A: Cluster Bounding Boxes
- Cluster mackerels: points within 8000 units distance form same cluster
- Use union-find or simple connected component
- For each cluster: compute bbox, expand 300-600 units in all directions
- Score = spatial_query(rect) - cost

### Strategy B: Multi-Rectangle Union  
- Find 5-8 top mackerel locations by local density (count within 2000x2000)
- Around each: create 1200x1200 or 1800x1800 rectangle
- Output all vertices of all rectangles as single polygon

### Strategy C: Ridge Following
- Sort mackerels by x-coordinate
- Find runs: 60+ points where y differs by < 4000 between consecutive
- Build long horizontal rectangle along run
- Repeat for y-sorted, find vertical runs
- Combine top 2-3 ridges

### Strategy D: Dense Region Expansion
- Scan 1000x1000 grid cells
- If (mackerels / max(sardines+1, 1)) > 1.5: expand
- Expand 4-directionally while ratio > 1.0
- Form bounding box rectangle

### Strategy E: Randomized Grid
- Pick 5 random (x,y) in [0,100000]
- For each: try rectangles 800x800, 1200x1200, 1600x1600 centered there
- Score by density estimate, pick best

## Phase 3: Aggressive Local Search

For each of top 3 candidate polygons:
- Initialize best_poly = candidate
- For iteration 1 to 4:
  * For each edge (p1, p2):
    - Try shifts of p1, p2 by ±150, ±300, ±450, ±600 in x and y
    - Estimate new score using spatial queries
    - Track best shift per edge
  * Apply best shifts to get refined polygon

## Phase 4: Validation

- Check vertex count: 4 to 1000
- Check perimeter: <= 400,000
- Check coords: all in [0, 100000]
- Check self-intersection: no crossing edges
- Output best polygon (or last valid one)

## Time Budget

Total per evaluation < 2.0 seconds. Strategies parallelizable.
Use fast spatial queries (O(1) per cell with precomputed grids).
