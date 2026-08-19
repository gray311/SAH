---
name: fish-polygon-constructor
description: A playbook for constructing axis-aligned polygons that wrap high-mackerel, low-sardine regions.
---

# Axis-Aligned Polygon Constructor

## Algorithm
1. Bucket fish into 1000x1000 grid cells.
2. Score each cell: mackerel_count - sardine_count.
3. Merge adjacent positive-score cells into regions.
4. For each region, compute bounding box.
5. Build polygon: (min_x,min_y) -> (max_x,min_y) -> (max_x,max_y) -> (min_x,max_y) -> (min_x,min_y).
6. Expand bounding boxes outward 1-5% if beneficial, staying within perimeter/vertex limits.

## Validation Rules
- Perimeter must be <= 400000
- Vertices must be <= 1000
- Coordinates must be in [0, 100000]
- If limits exceeded, merge smaller regions or reduce expansions

## Edge Cases
- If no positive-score regions exist: output a small 4-vertex polygon with score >= 1
- If regions are too far apart: output a single large merged rectangle
