---
name: discovery-optimization
description: "Stratified search for polygon optimization. Try trivial shapes first (rectangles, octagons), then basic rectangles, then sparse grid Laplacian flow if time permits. Use parallel restarts (5-8) with light hill climbing (\u00b110 shifts, 2-3 rounds). Always ensure valid output."
---

# Stratified Polygon Search Strategy

## Phase 1: Trivial Baselines (instant, must run)
- Try 100x100 square at (0,0)
- Try 8-vertex octagon expanding to ~200x200
- Output best of these if no time for more

## Phase 2: Basic Rectangle Generation (if time permits, ~0.5s)
- Generate 5-10 rectangles with random sizes 50-300, positions 0-70000
- Try expanding from (0,0) by adding width/height
- Each rectangle: simple 4 vertices, check perimeter and bounds

## Phase 3: Sparse Grid Laplacian Flow (if time permits, ~1.0-1.5s)
- Build 50x50 sparse grid at coordinates where fish exist
- Mark mackerel cells (+1), sardine cells (-1)
- Run 50 iterations of Laplacian relaxation: avg neighbors, then threshold
- Find connected components with net positive score
- Build axis-aligned hull around each component
- Try combining top 2 components if possible

## Phase 4: Lightweight Hill Climbing (if time permits, ~0.3s)
- For each candidate polygon:
  - For 3 random edges, try vertex perturbations ±10, ±20
  - Keep improvement, repeat 2 times max
  - Stop early if no improvement in 2 tries

## Phase 5: Parallel Restarts (not sequential!)
- Generate 5-8 independent candidate polygons in parallel
- Each restart picks: random seed point, random size 50-400
- Build simple rectangle from seed, light hill climb 2 rounds
- Track best valid polygon across all restarts

## Phase 6: Output
- Always output at least the trivial baseline (guaranteed valid)
- Output best valid polygon found
- Ensure: 4-1000 vertices, all coords in [0,100000], perimeter ≤ 400000

## Time Management
- If < 1.0s elapsed: stop and output best found
- If < 1.5s elapsed: try Phase 3
- If < 1.8s elapsed: try Phase 4-5
- Never exceed 1.9s (0.05s safety margin)
