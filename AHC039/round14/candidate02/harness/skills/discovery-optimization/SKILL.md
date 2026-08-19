---
name: discovery-optimization
description: "Union-of-rectangles strategy with fine-grained spatial analysis. Build\nhistogram of fish positions, identify mackerel-dense regions, generate\nbounding boxes, use probe_union_rects to guide rectangle adjustments,\ndeep local search with expand/merge operations, 20-30 restarts."
---

# Union-of-Rectangles Strategy for Axis-Aligned Polygon Optimization

## Overview
Instead of grid-based corridor expansion, we use fine-grained spatial
analysis to identify mackerel-dense regions and construct the polygon as
a union of axis-aligned rectangles.

## Phase 1: Fine-Grained Spatial Analysis
- Read all fish positions (N=5000 mackerels + N=5000 sardines)
- Build a spatial histogram (e.g., 1000x1000 grid or adaptive binning)
- For each bin, count mackerels (M) and sardines (S)
- Compute density score = M - S
- Identify top regions with positive score

## Phase 2: Bounding Box Generation
- For each top region, compute its axis-aligned bounding box
  (min_x, max_x, min_y, max_y)
- These boxes form initial candidate rectangles
- Each rectangle has integer coordinates in [0, 100000]

## Phase 3: Union-of-Rectangles Construction
- Combine multiple rectangles into a single orthogonal polygon
- The union of rectangles naturally forms an axis-aligned polygon with
  edges parallel to axes
- Merge adjacent rectangles when beneficial
- Remove internal boundaries (holes) if they reduce score

## Phase 4: Probe-Guided Local Search
Use probe_union_rects (cheap probe tool) to guide refinements:

For each candidate union-of-rectangles:
1. For each rectangle:
   - Try expanding each side by +/-5, +/-10, +/-20, +/-50 units
   - Try shrinking each side by same amounts
   - Keep changes that improve probe score
2. Try merging adjacent rectangles (combines overlapping/adjacent regions)
3. Try splitting large rectangles into smaller ones (reduces sardine
   exposure at edges)
4. Remove rectangles with consistently negative contribution
5. Repeat 5-8 rounds of refinement

## Phase 5: Multiple Restarts
- Run 20-30 restarts with different random seeds
- Each restart: random seed points -> bounding boxes -> refine -> output
- Track best polygon across all restarts

## Phase 6: Validation and Output
- Ensure polygon is valid: 4 <= vertices <= 1000, integer coords [0,100000]
- Perimeter <= 400,000, no self-intersection
- Output format: m vertices, then each vertex coordinates

## Why This Works Better
- Fine-grained spatial analysis captures local fish distributions more
  accurately than coarse grids
- Union-of-rectangles naturally forms axis-aligned polygons
- Probe-based search enables rapid exploration of shape space
- Multiple restarts ensure diversity and avoid local optima
