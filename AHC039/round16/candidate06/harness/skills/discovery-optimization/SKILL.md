---
name: discovery-optimization
description: "Coordinate-binning rectangle optimizer. Bin fish into 400x400 grid, grow rectangles from high-score bins, use directional growth for L-shapes, combine collinear rectangles, hill climb with \u00b110..20 shifts, 8 restarts."
---

# Coordinate-Binning Rectangle Optimization Strategy

## Phase 1: Coordinate Binning
- Create 400x400 grid over [0,100000]² (cell_size = 250)
- For each fish, increment bin at (x/250, y/250)
- Compute bin score = mackerels - sardines
- Identify top 8 bins with score > 0

## Phase 2: Rectangle Proliferation
For each top bin:
- Grow rectangle: start from bin center, expand step-by-step in all 4 directions
- At each expansion step, compute rectangle score using bin sums
- Try multiple sizes: small (100x100), medium (200x200), large (up to bounds)
- For each size, compute score and track best

## Phase 3: Directional Growth
From best rectangle found:
- Try extending in single directions (N, S, E, W) to create L-shapes
- Each extension adds a new rectangle adjacent to current shape
- Continue while: marginal gain > 0, total perimeter < 400,000, vertices < 1000
- This captures fish in connected regions efficiently

## Phase 4: Straight-Line Unions
- Find multiple rectangles that share a common edge (collinear adjacent)
- Union them into a single rectangle (no overlap, just side-by-side)
- This reduces perimeter penalty
- Try all pairs of adjacent high-scoring rectangles

## Phase 5: Hill Climbing
For each candidate polygon:
- For each vertex, try shifts: ±10, ±20 units (in x or y direction, whichever increases freedom)
- Score each variant using bin sums (O(1) per query)
- Repeat 2 refinement rounds
- Keep best improvement

## Phase 6: Restarts
- 8 restarts with diverse seeds:
  * Top 3 bins
  * Corners of bounding box (0,0), (0,100000), (100000,0), (100000,100000)
  * Best rectangle from first restart + random offset (±3000)
- Each restart explores single rects, L-shapes, unions
- Output best polygon

## C++ Implementation Notes
- Use coordinate binning for O(1) score queries
- Binning pre-computation: O(N) at startup
- Rectangle query: sum bins covered by rectangle (efficient with inclusion-exclusion)
- Total time per evaluation: < 1.8s
- All coordinates integers, validate no self-intersection
