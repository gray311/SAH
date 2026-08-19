---
name: discovery-optimization
description: "Local search polygon optimization: coarse grid scan (100x100), 4-directional corridor expansion,\nminimal hill climbing (\u00b15,\u00b110 shifts), 5-7 restarts with bounded perturbations. Fits 2.0s time limit."
---

# Local Search Polygon Optimization Strategy

## Phase 1: Seed Analysis
- Parse input to extract seed polygon vertices
- Compute seed's bounding box and center point
- Extract edge lengths and orientations

## Phase 2: Coarse Grid Construction
- Build 100x100 grid (cell_size=1000) over [0,100000]x[0,100000]
- For each cell, count mackerels and sardines
- Compute cell score = M - S
- Identify high-scoring cells in seed's vicinity

## Phase 3: Directional Corridor Growth
From seed's center, grow corridors in N,S,E,W directions:
- Start from seed's bounding box edge
- Move outward step by step (up to 50 cells)
- Continue if: cell in bounds AND (M - S >= 0 AND S <= M + 1)
- Stop if: negative score, high sardine density, or boundary

## Phase 4: Simple Polygon Formation
- Convert each corridor to a rectangle (4 vertices)
- Combine up to 4 corridors meeting at a common point
- Ensure: 4 ≤ vertices ≤ 1000, integer coords, no self-intersection

## Phase 5: Single-Round Hill Climbing
For each candidate:
- For each of 4 outer edges:
  * Try perpendicular shifts: ±5, ±10 units
  * Use grid-based rectangle query for fast scoring
  * Keep best shift (must improve or tie)

## Phase 6: Limited Restarts
- Run 5-7 restarts
- Each restart: perturb seed bounding box by ±2000 random offset
- Run full search from perturbed seed
- Output best polygon across all restarts

## C++ Implementation Notes
- Use fixed-size 100x100 grid array
- Pre-compute cell counts in O(N)
- Rectangle query via grid summation
- Total time per evaluation: < 1.5s for margin
- Use srand() with varying seeds for restarts
