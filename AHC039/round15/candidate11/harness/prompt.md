You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL: The seed is stuck at ~2.48. The previous grid-based approach (500-unit cells) is too coarse and fails to capture local density variations.

NEW STRATEGY - Multi-Strategy Geometric Search with Fine-Grained Analysis:

PHASE 1 - Direct Coordinate Analysis:
  - Parse fish coordinates directly from input (no coarse grid binning)
  - Build spatial index (hash map) for O(1) fish counting in rectangles
  - Compute 2D density: for each 1000x1000 cell, count mackerels vs sardines

PHASE 2 - Multi-Construction Pipeline (5+ strategies per evaluation, <2.0s total):
  
  Strategy A - Cluster Bounding Boxes:
    * Group mackerels by clustering (points within 8000 units form a cluster)
    * For each cluster, compute bounding box and expand by 300-600 units
    * Create rectangle; estimate score using spatial index
    * Generate 2-3 such rectangles from distinct clusters

  Strategy B - Multi-Rectangle Union:
    * Pick 5-8 top mackerel coordinates (by local density)
    * Create separate 1200x1200 or 1800x1800 rectangles around each
    * Union them (output all vertices of all rectangles)
    * This creates multi-lobed polygon

  Strategy C - Directional Ridge Following:
    * Sort mackerels by x, find runs of 60+ consecutive within y-tolerance 4000
    * For each run, build long rectangle following the x-projection
    * Repeat for y-coordinate runs
    * Combine longest 2-3 ridges

  Strategy D - Dense Region Expansion:
    * Find regions with mackerel-to-sardine ratio > 1.5 in 1000x1000 cells
    * From each such region, expand in all 4 directions until ratio drops below 1.0
    * Form rectangle from expansion bounds

  Strategy E - Randomized Grid Exploration:
    * Generate 5 random points, for each try rectangle sizes: 800x800, 1200x1200, 1600x1600
    * Pick best rectangle by estimated score (area * density - estimated sardines)

PHASE 3 - Aggressive Local Optimization:
  - For top 3 candidate polygons from above:
    * Try edge shifts of ±150, ±300, ±450, ±600 units (larger than previous ±25)
    * Use spatial index for fast score estimates
    * Keep best shifts per edge (up to 5 iterations)

PHASE 4 - Validation and Output:
  - Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
  - No self-intersection (use simple edge-crossing check)
  - Output single best polygon (or last one tried if tied)

Tools:
  - edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing multi-strategy search
  - evaluate_solution: Run C++ program, get score
  - probe_solution: NOT useful - need full evaluation for accurate scoring
  - finish: Submit when you have 5+ construction strategies with aggressive local search
