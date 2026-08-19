You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Seed-based local search with bounding-box scoring.

PHASE 1 - PARSE INPUT:
  - Read fish coordinates from input (first N mackerels, next N sardines)
  - Build two hash sets for O(1) point lookups

PHASE 2 - INITIAL POLYGON:
  - Start with a simple 4-vertex rectangle covering extreme points
  - Ensure axis-aligned, valid polygon (4 <= vertices <= 1000, perimeter <= 400000)

PHASE 3 - BOUNDING BOX SCORE (fast approximation):
  - For a candidate polygon, compute its bounding box [min_x, max_x] x [min_y, max_y]
  - Count mackerels where min_x <= x <= max_x and min_y <= y <= max_y
  - Count sardines similarly
  - Score = mackerel_count - sardine_count + 1
  - Use this for fast ranking during search

PHASE 4 - LOCAL SEARCH:
  - From current polygon, try vertex perturbations: for each vertex, try offsetting by ±5, ±10, ±15
  - Keep perturbations that improve the bounding-box score
  - Repeat until no improvement or 20 iterations

PHASE 5 - MULTIPLE SHAPE FAMILIES:
  - Try different polygon families: rectangles, L-shapes, U-shapes, and clusters
  - For each family, run Phase 4 local search
  - Return best overall polygon

OUTPUT: Valid polygon vertices (m on first line, then m lines of "x y")
Ensure execution < 2.0s per evaluation.
