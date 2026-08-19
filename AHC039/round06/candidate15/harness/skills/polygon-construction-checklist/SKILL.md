---
name: polygon-construction-checklist
description: Practical checklist for constructing axis-aligned polygons to maximize mackerel - sardine score in the fishery task. Use this when designing/editing C++ code.
---

# Axis-Aligned Polygon Construction - Practical Guide

## Understanding the Problem
- Score = max(0, mackerels_inside - sardines_inside + 1)
- Each mackerel captured: +1 point
- Each sardine captured: -1 point (released back)
- Goal: maximize the net difference (a - b + 1 where a=mackerels, b=sardines)

## Initial Strategy: Bounding Box of Mackerels
1. Find min_x, max_x, min_y, max_y of ALL mackerels (not all fish)
2. Create rectangle: vertices at (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
3. This rectangle covers 100% of mackerels but may also catch sardines
4. Calculate score and use as your baseline

## Optimization: Avoid Sardines
1. Consider "L-shaped" or "U-shaped" polygons that wrap around sardine clusters
2. Use multiple smaller rectangles instead of one large rectangle
3. Test two variants: (a) full mackerel rectangle, (b) sardine-excluding variant
4. Choose the one with better score

## Time Management (CRITICAL)
- Total time limit: 2.0 seconds with 0.1s safety margin
- Each evaluation should complete in 0.8-1.5 seconds
- If code approaches timeout, output current best polygon immediately
- Use simple data structures: std::vector instead of heavy containers
- Limit search iterations: 10-50 max (not 1000+)
- Add early exit if time limit approached

## Polygon Validity Checks
- Edges must be axis-aligned (dx=0 OR dy=0, not both nonzero)
- Max 1000 vertices (4-1000 is acceptable)
- Max perimeter 400,000 (calculate before output)
- No self-intersection (axis-aligned rectangles don't intersect themselves)
- All vertices must have distinct coordinates

## Common C++ Patterns
```cpp
// Simple axis-aligned rectangle
std::vector<Point> poly = {
    {min_x, min_y}, 
    {max_x, min_y}, 
    {max_x, max_y}, 
    {min_x, max_y}
};
// Check perimeter
long long perim = 2LL * (max_x - min_x) + 2LL * (max_y - min_y);
if (perim > 400000) { /* adjust coordinates */ }
```

## Recovery When Score Drops
1. Note the current score and validity
2. REVERT to best_so_far program immediately
3. Try a DIFFERENT polygon construction strategy entirely
4. Don't keep tweaking the same failing approach
5. Use analyze_fish to understand what went wrong

## Search Loop Design
- Outer loop: try different polygon shapes/strategies (5-10 variants)
- For each variant, construct polygon and evaluate
- Keep track of best score and corresponding polygon
- Use timer to ensure each eval completes in time
- If time limit approached, output current best immediately

## Quick Score Estimation (for debugging)
- Manually calculate expected score from your polygon
- Check: does polygon cover all known mackerel coordinates?
- Check: how many sardine coordinates fall inside?
- This helps diagnose if C++ implementation is correct
