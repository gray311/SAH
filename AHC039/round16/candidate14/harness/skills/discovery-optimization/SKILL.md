---
name: discovery-optimization
description: "Rectangle-first search with probe-based ranking. Generate 20 random rectangles per restart from mackerel-dense grid cells, use probe_solution to rank them cheaply, hill climb top 5 with \u00b15/\u00b110 edge shifts, evaluate the best of 30 restarts."
---

# Rectangle Optimization Strategy

## Phase 1: Grid Construction
- Build 100x100 grid (cell_size=1000) over [0,100000]x[0,100000]
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify top 30 cells with highest positive score

## Phase 2: Rectangle Generation
For each restart (30 total):
- From the top 30 cells, randomly select 5 seeds
- For each seed, generate 20 random rectangles:
  * Center at or near the seed cell
  * Random width and height: 200-800 units (ensures perimeter <= 3200)
  * Clamp to [0, 100000] bounds
  * Record all 100 rectangles for this restart

## Phase 3: Probe-Based Ranking
- Use probe_solution to score all 100 rectangles (cheap, ~10s each)
- Keep track of probe scores for ranking

## Phase 4: Hill Climbing on Top 5
For each of the top 5 rectangles by probe score:
- Extract the 4 edge coordinates
- For each corner, try shifting it by ±5 and ±10 units in each axis-aligned direction
- Generate up to 16 variants per rectangle (8 corners × 2 shift amounts)
- Use probe_solution to score each variant
- Select the best variant

## Phase 5: Full Evaluation
- Use evaluate_solution on the single best rectangle after hill climbing
- This consumes 1 evaluation credit

## Phase 6: Multiple Restarts
- Repeat Phases 2-5 for 30 restarts with different random seeds
- Track the best score across all restarts
- Output the polygon corresponding to the best result

## Implementation Notes
- Use std::random_device for reproducible seeds
- Rectangle representation: 4 vertices in order (e.g., bottom-left, top-left, top-right, bottom-right)
- Perimeter check: ensure 2*(width+height) <= 400000
- Use probe_solution extensively before evaluate_solution to avoid wasting evaluations
