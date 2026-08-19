---
name: discovery-optimization
description: "Fast rectangle-based polygon construction. Build 100x100 grid, find top 10 high-score cells, create 5-10 rectangles of various sizes, combine nearby clusters, local hill climbing with \u00b110..20 shifts, 5-8 restarts for <1.5s execution."
---

# Fast Rectangle-Based Polygon Optimization

## Phase 1: Fast Grid Analysis
- Use 100x100 grid with cell_size=1000 (covers 0-100000 in 100 cells)
- For each cell, count mackerels and sardines from input
- Compute cell score = M - S
- Identify top 10 cells with highest positive score

## Phase 2: Rectangle Generation
For each top cell, generate rectangles centered on it:
- Try sizes: 50x50, 100x100, 150x150, 200x200, 250x250 units
- For each rectangle, compute score by summing all grid cells inside
- Calculate efficiency: score / (perimeter * area)
- Keep top candidates

## Phase 3: Cluster Combination
- Group nearby rectangles (centers within 300 units)
- For each group, compute combined bounding box
- Output vertices of combined polygon (or individual rectangles if separate)
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]

## Phase 4: Local Hill Climbing
For each candidate polygon:
- For each edge, try shifts ±10, ±20 units
- Use grid-based rectangle query for fast scoring
- Keep shift that maximizes M - S
- Repeat once more if improvement

## Phase 5: Few Random Restarts
- Run 5-8 restarts with different random seeds
- Each restart:
  * Randomly perturb top cell selection (±200 units)
  * Pick 3-4 perturbed top cells
  * Build 2-3 rectangles per cell
  * Combine and hill climb
- Track best polygon across all restarts

## Phase 6: Validation
- Output valid polygon only
- Check: 4-1000 vertices, integer coords in [0,100000], no self-intersection
- Use O(n²) edge crossing check for self-intersection

## C++ Implementation Notes
- Use fixed-size 100x100 grid array for O(1) access
- Pre-compute all cell scores in O(N) at startup
- Rectangle query = sum of grid cells covering rectangle
- Total time per evaluation: < 1.5s with efficient operations
- Use std::random_device for seed generation
