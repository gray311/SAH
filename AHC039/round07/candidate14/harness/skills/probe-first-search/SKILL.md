---
name: probe-first-search
description: Probe-first search for polygon optimization - generate many candidates, quickly rank with 5% sampling (analyze_polygon), confirm top 3-5 with full evaluation, then refine. Avoids wasting full evals on poor polygons.
---

# Probe-First Search Strategy for Fish Capture

## Core Idea
Instead of evaluating each polygon candidate fully (2s per eval), use
analyze_polygon (5% sampling, ~10ms) to rapidly rank thousands of candidates.
Only spend full evals on top 3-5.

## Algorithm
1. Build spatial index (KD-tree or grid) - O(N log N)
2. Generate 100-200 polygon candidates in 0.5s
   - Random rectangles
   - L-shapes capturing mackerel clusters
   - Stepped polygons along density contours
3. Probe ALL candidates with analyze_polygon in 0.8s
   - Sample 5% of 10000 fish = 500 fish
   - Fast approximate score
4. Select top 3-5 by probe score
5. Full evaluation on best candidate - 2s
6. Refine: perturb edges 1 to 50, re-probe, keep improvements
7. Repeat steps 2-6 until time budget exhausted

## Why This Works
- Full evals are expensive: 30 budget, 2s each -> can only try 10-15 candidates
- Probes are cheap: 100 budget, 10ms each -> can try 1000+ candidates
- 5% sampling preserves relative ranking for axis-aligned polygons
- Focuses precious full evals on most promising candidates

## Implementation Checklist
- analyze_polygon tool: sample 5% fish, count types, return score
- generate_candidates(): produce 100+ polygon variants
- probe_all(): call analyze_polygon on all candidates
- select_top_k(): pick top 3-5 by probe score
- refine_best(): edge perturbations with probe feedback
- main loop: repeat until timeout
- spatial index: KD-tree or grid for O(1) rectangle queries
