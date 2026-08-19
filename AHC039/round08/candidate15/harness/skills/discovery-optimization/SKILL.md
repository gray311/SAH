---
name: discovery-optimization
description: "Optimize C++ polygon by targeting isolated mackerels. Find mackerels with no nearby sardines, generate tight boxes around them, expand while excluding sardines, and combine if beneficial."
---

# Targeted Single-Fish Capture Strategy

## Core Idea
Instead of large clusters, find isolated mackerels (those with no sardines within 300 units) and capture them with tight polygons.

## Phase 1: Isolation Detection
- Parse all fish into (x,y,type) arrays
- For each mackerel, compute min distance to any sardine
- Mark mackerel as "isolated" if min_sardine_distance > 300
- Collect all isolated mackerels (expect 20-50 on average)

## Phase 2: Tight Box Generation
For each isolated mackerel at (x,y):
- Generate candidate boxes: 1x1, 3x3, 5x5 centered at (x,y)
- For each box, verify it contains NO sardines (distance from box to nearest sardine > 0)
- Score = number of mackerels in box - number of sardines in box + 1
- Keep boxes scoring >= 2

## Phase 3: Controlled Expansion
For each valid tight box:
- Try expanding in 4 directions (up, down, left, right) by 1, 2, ..., 50 units
- After each expansion, check: does it include any new sardines?
- If no sardines added, keep the expansion
- Continue until hitting a sardine or timeout
- Track the best expansion for each seed box

## Phase 4: Combination Strategy
- Sort all expanded boxes by score
- Try combining top 2-3 boxes into one polygon (union of rectangles)
- Verify combined polygon is valid (no self-intersection, perimeter < 400000)
- Score the combined polygon

## Phase 5: Hill Climbing Refinement
For the best candidate from Phase 4:
- For each edge, try shifts ±1..10 in x or y direction
- Keep shifts that improve score or maintain score while increasing perimeter efficiency
- Repeat 2-3 rounds

## Phase 6: Random Restarts
- Run Phases 1-5 with 10 different random seeds
- In each restart, randomly select a subset of isolated mackerels
- Track the global best across all runs

## Implementation Notes
- Use O(N) distance computation (N=5000, so 5000*5000 = 25M ops, acceptable in 2s)
- Pre-compute sardine positions in a hash set for O(1) containment checks
- Use bounding box intersection for fast sardine exclusion checks
- Total time per evaluation: ~1.5-1.8s, leaving margin for final output
