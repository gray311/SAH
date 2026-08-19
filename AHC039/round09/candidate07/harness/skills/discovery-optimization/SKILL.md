---
name: discovery-optimization
description: "Direct cluster targeting with minimal polygon. Find densest mackerel cluster in 500x500 grid, build tight rectangle around it with small edge shifts (\u00b12,\u00b14,\u00b16,\u00b18), run 5-10 restarts."
---

# Direct Cluster Targeting Strategy

## Phase 1: Fine Grid Analysis
- Use 500x500 grid with cell_size=200 (covers 0-100000)
- For each cell, count mackerels and sardines from input
- Compute cell score = M - S
- Find the cell with highest positive score

## Phase 2: Minimal Polygon Construction
- From the densest cell, build a minimal axis-aligned rectangle
- Start with cell boundaries (4 vertices)
- Only expand to capture more mackerels if score improves and sardine count stays low

## Phase 3: Targeted Hill Climbing
- For each edge, try shifts: ±2, ±4, ±6, ±8 units
- Use fine-grid rectangle query for scoring
- Keep shift that maximizes M - S
- Repeat until no improvement

## Phase 4: Focused Restarts
- Run 5-10 restarts with different random seeds
- Each restart: pick a random subset of cells, find densest, build minimal polygon
- Output single best polygon

## C++ Implementation Notes
- Use fixed-size 500x500 grid for O(1) access
- Pre-compute all cell scores in O(N) at startup
- Focus on single cluster, not multi-cluster corridors
- Keep polygon small to minimize sardine capture
