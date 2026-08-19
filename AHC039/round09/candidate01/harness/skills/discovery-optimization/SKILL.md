---
name: discovery-optimization
description: "Coarse regional analysis with rectangle mutation. Use 50x50 grid (cell_size=2000) to find mackerel-dense regions, build large axis-aligned rectangles, combine into multi-lobed polygons, edge refinement with \u00b1100..300 shifts, 25-30 restarts."
---

# Regional Rectangle Strategy for Polygon Optimization

## Overview
Instead of fine-grained cell corridors, use coarse regional analysis to identify broad mackerel-dense areas and build large axis-aligned rectangles that capture multiple clusters while avoiding sardine penalties.

## Phase 1: Coarse Grid Construction
- Use 50x50 grid over [0,100000]x[0,100000] (cell_size=2000)
- For each cell, count mackerels (M) and sardines (S)
- Compute cell score = M - S
- Identify top 20 cells with highest positive score

## Phase 2: Rectangle Building
For each top cell, attempt to build a rectangle:
- Start from seed cell center
- Expand each direction (N,S,E,W) by trying larger distances
- Track cumulative score as rectangle grows
- Stop when: perimeter > 400,000, score drops > 50%, or boundary reached
- Ensure: 4 <= vertices <= 1000, coords in [0,100000]

## Phase 3: Multi-Rectangle Combination
- Select 2-5 best rectangles from Phase 2
- Compute their union (handle overlaps by merging)
- Convert to single polygon with no self-intersection
- Can form L-shapes, multi-lobed structures

## Phase 4: Edge Position Refinement
For each candidate polygon:
- For each edge, try shifts: ±100, ±200, ±300 units
- Use rectangular score estimation for fast evaluation
- Keep shift that maximizes M - S
- Repeat 2 refinement rounds

## Phase 5: Regional Diversity Search
- Run 25-30 restarts with different random seeds
- Each restart: 
  * Randomly perturb top cell selection
  * Pick random subset of 3-5 top cells
  * Build rectangles, combine, refine
- Output single best polygon across all restarts

## Implementation Notes
- Use fixed-size 50x50 grid array for O(1) access
- Pre-compute all cell scores at startup
- Rectangle score = sum of grid cells covered
- Use efficient O(1) rectangle queries
- Total time per evaluation: < 2.0s
- Include simple self-intersection check (edge-pair collision)
