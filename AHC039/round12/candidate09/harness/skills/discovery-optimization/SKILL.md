---
name: discovery-optimization
description: "KD-tree enhanced polygon optimization. Use seed's KD-tree efficiently, add sparse grid at high-density regions only, 5 focused restarts with \u00b13,\u00b17,\u00b111 shifts, 2 hill climb rounds."
---

# KD-Tree Enhanced Polygon Strategy

## Phase 1: Data Structures (Key Improvement)
- Build KD-tree from all fish positions (seed's O(N log N) approach)
- Add sparse 25x25 grid ONLY at cells with >3 mackerels (not full 200x200)
- KD-tree handles exact rectangle queries in O(log N)
- Sparse grid handles quick density checks in O(1) where needed

## Phase 2: Focused Search (Key Improvement)
- Identify top 30 high-density mackerel cells from KD-tree queries
- Run 5 restarts (not 15-20) with random selections from these cells
- Each restart: try 2-3 starting cells, build initial polygon candidates
- Save ~70% time vs seed's 15-20 restarts

## Phase 3: Efficient Hill Climbing (Key Improvement)
For each candidate polygon:
- For each edge (up to 1000 vertices):
  * Try shifts: ±3, ±7, ±11 units (smaller than seed's ±5..25)
  * Use KD-tree rectangle query for O(log N) scoring
  * Keep shift maximizing mackerels - sardines
- Repeat 2 rounds (not 3) - faster convergence with smaller steps

## Phase 4: Polygon Construction
- Ensure 4 <= vertices <= 1000
- Integer coordinates in [0,100000]
- Perimeter <= 400,000
- No self-intersection (KVH check)

## Phase 5: Final Selection
- Track best polygon across all 5 restarts
- Output single best polygon
- Total time per evaluation: < 2.0s

## Why This Works
- Seed's KD-tree is already efficient; we enhance, don't replace
- Sparse grid augmentation only where high density exists
- Fewer restarts (5 vs 15-20) saves significant time
- Smaller perturbations (±3,±7,±11) converge faster per iteration
- Fewer hill climbing rounds (2 vs 3) reduces computation
