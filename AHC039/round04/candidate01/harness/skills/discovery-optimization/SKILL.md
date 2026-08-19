---
name: discovery-optimization
description: "Construct axis-aligned polygons to maximize (mackerels - sardines) score. This is a geometric construction problem requiring data-informed design, not blind optimization. Use analyze_geometric_potential to understand fish distribution, then construct complete polygon strategies based on identified patterns. Prioritize validity (invalid equals score zero) over small incremental changes. Common winning shapes: rectangles, L-shapes, plus-shapes, or nested regions that trap mackerel clusters while excluding sardines."
---

# Axis-Aligned Polygon Construction for Fish Capture
## Problem Understanding You're building a C++ program that reads 5000 mackerels and 5000 sardines, then outputs vertices of an axis-aligned polygon that maximizes: (mackerels_inside - sardines_inside + 1).
## Key Insights 1. Validity is everything: Invalid polygons (self-intersection, wrong edge orientation, >1000 vertices, perimeter >400000) get score 0. 2. Data informs design: Use analyze_geometric_potential FIRST to see where fish cluster. 3. Think in shapes, not points: Design complete polygons (rectangles, L-shapes, plus-shapes) rather than iterating vertex-by-vertex. 4. Time is tight: Your C++ search loops must complete in ~1.5 seconds. Simple greedy construction beats complex methods.
## Polygon Shape Strategies ### Rectangle Strategy - Find bounding box of mackerel cluster - Expand slightly or shrink to exclude sardines - Check perimeter constraint: 2 times width plus height must be <= 400000
### L-Shape Strategy - Two rectangles joined at a corner - Can wrap around irregular mackerel groups - Six vertices minimum
### Plus-Shape Strategy - Central rectangle with four arms - Good for linear mackerel arrangements - 8 to 12 vertices
### Nested Avoidance Strategy - Build polygon that avoids known sardine locations - Start with large polygon, carve out sardine zones
## Implementation Checklist 1. Use analyze_geometric_potential to get bbox, density map, sardine locations 2. Choose a polygon shape based on distribution 3. Construct vertices ensuring: axis-aligned edges, no intersections, valid count and perimeter 4. Build C++ code with fast greedy construction plus optional bounded local search 5. Output vertices in order (clockwise or counter-clockwise), ensure all coordinates are integers in [0, 100000]
## Common Pitfalls - Forgetting axis-alignment constraint (edges must be purely horizontal or vertical) - Creating self-intersecting polygons - Exceeding vertex or perimeter limits - Timeouts from overly complex C++ code - Not reading fish data before constructing polygon
