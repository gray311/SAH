You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The optimal solution is often a SINGLE large axis-aligned rectangle that encloses a dense cluster of mackerels while avoiding sardines.

SEARCH STRATEGY:

PHASE 1 - Baseline Rectangle Search (fast, high success):
  - Generate 50-100 random axis-aligned rectangles
  - Each rectangle: random center (0-100000), random width/height (1000-50000)
  - Compute score by scanning all fish points (O(N))
  - Track best rectangle

PHASE 2 - Grid-Guided Refinement (if Phase 1 exhausted time):
  - Build 50x50 grid (cell_size=2000) for finer resolution
  - Find top 10 cells with highest M-S score
  - For each top cell, try 9 surrounding cells as rectangle centers
  - Generate rectangles extending in all 4 directions from center
  - Score each candidate

PHASE 3 - Edge Perturbation (final polish):
  - For best rectangle, try perturbations of each corner by ±10, ±20, ±30
  - Keep perturbations that improve score
  - Ensure valid output (4 vertices, perimeter <= 400,000)

RUN 25 restarts with different random seeds. Output single best rectangle.

OUTPUT FORMAT: Exactly 4 vertices for a rectangle (minimum required).
Format: m\nx1 y1\nx2 y2\nx3 y3\nx4 y4 (in order around rectangle)

Time budget: < 1.9 seconds per evaluation. Prioritize Phase 1.
