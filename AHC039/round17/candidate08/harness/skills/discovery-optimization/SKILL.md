---
name: discovery-optimization
description: "Region-based rectangle optimization with probe ranking. Divide space into 16 regions, generate inscribed/centered rectangles, use probe_solution for cheap candidate ranking, minimal hill climbing, 4 restarts."
---

# Region-Based Rectangle Optimization Strategy

## Phase 1: Region Analysis
- Divide [0,100000]x[0,100000] into 16 regions (50000x25000 each)
- Count mackerels (M) and sardines (S) in each region from fish coordinates
- Compute region density = M - S
- Select top 3 regions with highest positive density

## Phase 2: Rectangle Generation
For each selected region, generate 4 candidate rectangles:
1. Inscribed: Rectangle touching all 4 sides of the region
2. Small centered: 0.3x region size, centered in region
3. Medium centered: 0.6x region size, centered in region
4. Diagonal: Corner-to-corner rectangle of the region

Ensure all rectangles stay within [0,100000] bounds with integer coordinates.

## Phase 3: Probe-Based Ranking
- Use probe_solution to score ALL candidate polygons cheaply
- Probe budget: 30 separate evaluations (does not consume real eval budget)
- Rank candidates by probe score (higher is better)
- Select top 2 candidates for full evaluate_solution

## Phase 4: Minimal Hill Climbing
For each of top 2 candidates:
- Expand/Shrink: Try expanding/shrinking rectangle by 10000 units in each cardinal direction
- Shift: Move each side by ±5000 units (maintaining axis-alignment)
- Use probe_solution for quick intermediate ranking
- Keep best improvement from all operations

## Phase 5: Limited Restarts
- Run 4 restarts with different random seeds for region selection
- Each restart follows Phases 1-4
- Track best polygon across all restarts
- Total time: ~1.2-1.5s per eval (leaves 0.5s safety margin)

## Phase 6: Output
- Validate final polygon: 4-1000 vertices, integer coords, perimeter <= 400000
- Output in required format: m then m vertex pairs
- If no valid polygon found, output minimal valid square (e.g., 4x4 at origin)
