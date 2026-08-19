---
name: rectilinear-polygon-optimizer
description: A strategy for optimizing rectilinear polygon construction for geometric scoring tasks. Use scan_horizontal_regions to find mackerel-rich y-bands, then build simple axis-aligned polygons covering those bands. Probe multiple variants before full evaluation.
---

# Rectilinear Polygon Optimizer Strategy

## Phase 1: Scan for high-density regions
1. Call scan_horizontal_regions to get y-bands sorted by mackerel ratio
2. Select top 3-5 bands with highest mackerel/sardine ratios
3. Determine x-range that covers most fish in these bands

## Phase 2: Build candidate polygons
Option A: Single rectangle
- Use min/max x and y from selected bands
- Check if perimeter < 400,000
- If too large, shrink bounds or use multiple smaller rectangles

Option B: Merged bands
- Combine adjacent y-bands into strips
- Connect them with vertical edges
- Result: a rectilinear polygon with fewer self-intersections

Option C: Concentric band polygons
- Build multiple nested polygons focusing on densest regions
- Use probe to test each nesting depth

## Phase 3: Probe and evaluate
1. Generate 3-5 variants (different rectangle sizes, band combinations)
2. Probe each variant (fast, cheap ranking)
3. Evaluate only the top 1-2 variants (full scoring)
4. Keep best, iterate with new insights

## Phase 4: Perimeter constraint handling
- Track total perimeter: sum of all edge lengths
- For simple rectangle: 2*(width + height)
- For complex polygon: sum(|dx| + |dy| for each edge)
- Stay under 400,000; if violated, reduce polygon size
- Vertices: 4-1000; typical is 8-16 for good coverage

## Phase 5: When probing yields low scores
- Expand polygon to cover more ground
- Try vertical strips instead of horizontal
- Consider the trade-off: covering more mackerels vs. including sardines
- Use probe to quickly test expansion strategies
