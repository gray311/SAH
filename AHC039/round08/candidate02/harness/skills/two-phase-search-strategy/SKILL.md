---
name: two-phase-search-strategy
description: Use two-phase search - Phase 1 extracts geometric anchors (bounding boxes, 2x2 blocks, centroid), Phase 2 generates multiple polygon patterns per anchor, Phase 3 hill climbs, Phase 4 combines best.
---

# Two-Phase Search Strategy for Mackerel-Sardine Polygon Optimization

## Why Two Phases?

Phase 1 is a quick O(N) analysis that identifies WHERE to focus the expensive Phase 2 search.
Without Phase 1, we waste time searching empty regions.

## Phase 1: Anchor Extraction (Must run first)

Compute these four anchors from all mackerel positions:
1. **Global Bounding Box**: minX, maxX, minY, maxY of all mackerels
2. **Top 5 2x2 Blocks**: Find 2x2 groups of consecutive mackerels - these are high-density regions
3. **Centroid**: Average position of all mackerels
4. **Edge-Filtered Box**: Shrink global box where sardines are within 200 units

These anchors take <0.1s to compute and guide all subsequent search.

## Phase 2: Pattern Generation per Anchor

For EACH anchor from Phase 1, generate THREE patterns:

**Pattern A: Tight Bounding Box**
- Simple rectangle from anchor's bounding box
- Fast to evaluate, good baseline

**Pattern B: Holed Bounding Box**
- Start with Pattern A
- For each sardine within 200 units of edges, create an indent
- Adds 2-4 vertices per sardine, outputs 6-10 vertices

**Pattern C: Corner-Heavy L-Shape**
- Find corner farthest from nearest sardine
- Cut off opposite side with 2 indents
- Outputs 6 vertices, captures dense corner region

## Phase 3: Hill Climbing Refinement

For each candidate polygon from Phase 2:
- For each edge (4-10 edges):
  - Try shifting inward by ±1, ±2, ..., ±15 units
  - Use grid query to estimate score
  - Keep improvements
- Repeat up to 2 refinement rounds

## Phase 4: Multiple Random Restarts

- Run Phases 1-3 with 3 different random seeds
- Perturb block detection, random indent positions
- Output SINGLE best polygon across all runs

## Time Budget Management

- Phase 1: <0.1s (must complete before Phase 2)
- Phase 2: <0.5s (generate ~15 candidates)
- Phase 3: <0.8s (hill climb top 5 candidates)
- Phase 4: <0.4s (combine and select best)
- Total: <2.0s with safety margin
