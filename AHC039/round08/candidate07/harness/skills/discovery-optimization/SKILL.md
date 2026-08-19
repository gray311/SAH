---
name: discovery-optimization
description: "Optimize via multi-pattern search: rectangle, L-shape, U-shape, stepped polygons with local edge refinement. Uses 100x100 grid for fast scoring. Sample 30+ candidates per pattern, optimize edges locally, output best valid polygon."
---

# Multi-Pattern Polygon Optimization

## Strategy: Generate multiple explicit polygon patterns, optimize edges locally, return best.

### Phase 1: Grid Setup
- Build 100x100 grid over [0,100000]² (cell_size=1000)
- For each cell, count mackerels (M) and sardines (S)
- Precompute prefix sums for O(1) rectangle queries

### Phase 2: Pattern Generation

**Pattern A: Rectangle**
- Slide a window over 5x5 cells (≈5000×5000 area)
- For each window, find tight bounding box of all fish inside
- Score = rectangle_score(minX, minY, maxX, maxY)

**Pattern B: L-Shape**
- Choose corner (cx, cy) in grid
- Choose arm widths (w1, w2) in cells (1-10 each)
- Form L: two rectangles sharing a corner
- Score using grid prefix sums

**Pattern C: U-Shape**
- Similar to L but with three arms
- Can exclude a sardine-rich region while keeping fish-rich areas

**Pattern D: Stepped Polygon**
- Start from a dense cell, step up/down/left/right
- Each step adds a segment, keep if score improves
- Limit to 10-15 segments

### Phase 3: Local Edge Optimization
For each candidate polygon:
- For each edge (4-20 edges):
  - Try shifting inward by +5, +10, +15, +20 units
  - Try shifting outward by -5, -10, -15, -20 units
  - Recompute score using grid query
  - Keep shift that improves score
- Repeat 2 rounds

### Phase 4: Random Restarts
- Run Phases 2-3 with 10 different random seeds (different window starts)
- Track best polygon across all runs

## C++ Implementation
- Use fixed 100x100 grid array
- Precompute 2D prefix sums for O(1) rectangle queries
- All patterns must produce valid axis-aligned polygons
- Output: m (vertices), then m lines of (x, y)
