---
name: discovery-optimization
description: "Grid-based rectangle exploration with sardine boundary optimization. Scan 100x100 grid, find candidate cells with positive M-S, expand into maximal rectangles, optimize boundaries to exclude sardines, combine rectangles, deep hill climb, 25 random restarts."
---

# Grid-Based Rectangle Exploration Strategy

## Phase 1: Grid Analysis
- Use 100x100 grid over [0,100000]x[0,100000] (cell_size=1000)
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify ALL cells with score > 0 as "candidate regions"

## Phase 2: Rectangle Expansion
For each candidate cell:
- Expand in all 4 cardinal directions (N, S, E, W)
- Build maximal rectangles that maintain positive net score
- Try multiple rectangle sizes: small (4x4), medium (10x10), large (50x50) cells
- Record rectangle vertices

## Phase 3: Boundary Optimization
For each rectangle candidate:
- Try shifting right edge by ±1, ±2, ±3 units to exclude boundary sardines
- Try shifting top edge by ±1, ±2, ±3 units
- Use grid-based scoring for each variant
- Keep variant with highest M - S

## Phase 4: Multi-Rectangle Combination
- Try combining 2-3 non-overlapping rectangles into one polygon
- Use "comb" or "crown" shapes to connect rectangles
- Ensure perimeter and vertex constraints

## Phase 5: Deep Hill Climbing
For each top candidate:
- For each edge, try shifts ±5, ±10, ±15, ±20 units
- Use grid-based rectangle query for fast scoring
- Repeat 5 refinement rounds

## Phase 6: Multiple Random Restarts
- Run 25 restarts with different random seed cell selections
- Each restart: pick 5 random candidate cells, build rectangles, combine, hill climb
- Output best polygon across all restarts

## Implementation Notes
- Use O(1) grid access for fast rectangle scoring
- Rectangle perimeter = 2*(width + height) in units
- Total perimeter must be <= 400,000
- All coordinates in [0,100000]
- Use KVH validator for self-intersection check
