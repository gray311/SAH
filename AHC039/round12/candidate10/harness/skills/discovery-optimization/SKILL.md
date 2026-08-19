---
name: discovery-optimization
description: "Rectangle union with KD-tree and probe-based screening. Build sparse grid, use probes to rank candidate rectangles, combine into disjoint rectangles, deep hill climb with edge refinement, 25 restarts."
---

# Rectangle Union with Probe Screening

## Core Idea
Instead of corridor expansion, use **rectangle union**: find optimal axis-aligned rectangles that cover mackerel-rich areas, combine up to 5 disjoint rectangles.

## Phase 1: Sparse Grid Sampling
- 100x100 grid over [0,100000]x[0,100000] (cell_size=1000)
- For each cell, use probe_solution with subsampling to estimate M and S
- Track cell score = M - S
- Identify top 30 cells

## Phase 2: Rectangle Construction
For each top cell, expand into a rectangle:
- Start from cell center
- Expand E/W until: boundary, 0 score, or another rectangle
- Expand N/S similarly
- Minimum rectangle: 200x200
- Maximum rectangles: 5 (to stay within perimeter budget)

## Phase 3: Probe-Guided Ranking
For each candidate rectangle configuration:
1. Call probe_solution for fast approximate scoring (~10s)
2. Try edge shifts: +/-10, +/-50, +/-100 units in each direction
3. Keep top 3 configurations by probe score
4. Evaluate the best 1-2 with evaluate_solution

## Phase 4: KD-Tree Hill Climbing
- Each rectangle uses KD-tree for O(log N) exact fish counting
- Binary search for optimal edge positions
- Try merging adjacent rectangles if (M-S) increases

## Phase 5: Restart Strategy
- 25 restarts with different seeds
- Perturb top-30 cell selection randomly
- Always keep global best

## Implementation Notes
- Use KD-tree for efficient rectangle queries (already in seed)
- Probe-based screening reduces evaluation budget waste
- Output valid polygon: list of rectangles as consecutive vertices
- Perimeter = sum of perimeters of all rectangles
