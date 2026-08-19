---
name: discovery-optimization
description: "Direct pair-based rectangle search: pick mackerel pairs, build minimal enclosing rectangle, count fish, score. Simple, fast, valid polygons."
---

# Pair-Based Rectangle Optimization Strategy

## Core Idea
Instead of building complex multi-lobed polygons, focus on simple rectangles that enclose exactly 2 mackerels with 0 sardines. Score = 2 - 0 + 1 = 3.

## Algorithm
1. Parse all fish coordinates from input
2. For each pair of mackerels:
   - Compute bounding rectangle: x_min=min(x1,x2), x_max=max(x1,x2), y_min=min(y1,y2), y_max=max(y1,y2)
   - Ensure rectangle is valid (not degenerate, within bounds)
   - Count mackerels and sardines inside (inclusive)
   - Score = m - s + 1
3. Track best rectangle across all pairs
4. Also try single-mackerel degenerate rectangles (width/height = 1) as fallback
5. Output best valid rectangle (4 vertices)

## Implementation Details
- Use O(N^2) pair enumeration but with random sampling to save time
- Use coordinate compression or grid for O(1) point-in-rectangle queries if needed
- Early termination when time budget exhausted
- Always output 4-vertex axis-aligned rectangle
- Validate perimeter <= 400,000 (always true for N=5000, coords <= 100000)

## Why This Works
- Simple geometry: rectangles never self-intersect
- Fast construction: O(1) per pair
- Many successful cases: with random fish distribution, many 2-mackerel pairs have no sardines nearby
- Score = 3 is achievable and stable
- Within all constraints: 4 vertices, integer coords, valid perimeter

## Time Optimization
- Random sample pairs instead of exhaustive enumeration
- Use spatial indexing for faster containment checks
- Early stop when time < 0.1s
- Parallel pair processing if beneficial

## Fallback
If no 2-mackerel rectangle found with 0 sardines, try:
- Single mackerel with 1x1 rectangle (score = 1-0+1 = 2)
- Multiple small clusters
- Always ensure valid 4-vertex output
