---
name: multi-lobed-construction
description: Construct multi-lobed polygons by connecting multiple mackerel-dense regions via sardine-safe corridors.
---

# Multi-Lobed Polygon Construction Guide

## Why Multi-Lobed?
Single-lobed polygons can only capture one cluster. By building 2-6 connected lobes, we capture multiple high-value regions while minimizing sardine overlap.

## Method

### Step 1: Grid-based Clustering
- Build 200x200 grid, count M and S per cell.
- Compute M-S per cell.

### Step 2: Seed Selection
- Pick top 3-6 cells with high M-S score (e.g., >= 10).
- These are your "seed islands".

### Step 3: Corridor Expansion
From each seed, expand in 4 directions using the rule:
  Continue if: (in bounds) AND (M >= S OR S <= M + 1)
  Stop if: S > M + 1 (sardine trap)

### Step 4: Polygon Assembly
Connect seeds via corridors:
- Chain: seed1 -> E to end -> S to seed2 -> W to seed3 -> N to seed1.
- Or nested/disjoint if connection costs high S.

### Step 5: Local Optimization
For each edge, shift by +/-10, +/-20, +/-30, +/-40, +/-50.
Use grid prefix sums for fast M-S scoring.
Repeat 2 refinement rounds.

### Step 6: Restarts
Run 12 restarts with random seeds. Output best.

## Key Success Factors
- Multi-lobed > single-lobed for this task (more clusters = more score).
- Aggressively avoid S > M + 1 regions.
- Large edge shifts (+/-50) may be necessary due to coarse grid.
