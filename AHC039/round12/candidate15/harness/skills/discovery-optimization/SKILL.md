---
name: discovery-optimization
description: "Local search refinement around seed solutions. Use probe_solution for fast scoring, try edge shifts +1/-1..+10/-10, vertex insertions/deletions, corner rounding. 2-3 rounds of refinement, occasional strategic variations."
---

# Local Search Refinement Strategy

## Core Principle
The seed program already finds good solutions (~2.48 average). Your job is to refine, not rebuild.

## Phase 1: Baseline Generation
1. Parse input and construct an initial polygon (use seed's approach)
2. Validate: 4-1000 vertices, perimeter <= 400,000, integer coords [0,100000], no self-intersection
3. Run FULL evaluation to get baseline score

## Phase 2: Probe-Based Ranking
For each vertex (x,y):
- Generate perturbed polygons: shift vertex by +1, -1, +2, -2, +3, -3, +5, -5, +8, -8 units
- Use PROBE_SOLUTION to score each variant (fast, ~10s)
- Select top 10-20 candidates by probe score

## Phase 3: Deep Refinement
For top 3-5 candidates:
- Run FULL evaluation on each
- For each vertex in each candidate:
  * Try edge shifts: +1, -1, +2, -2, +3, -3, +5, -5, +8, -8, +10 units
  * Try adding vertex at midpoint of edges >500 length
  * Try removing collinear vertices
- Keep best improvements, repeat 2-3 rounds

## Phase 4: Strategic Variations (20 percent each)
- Outward expansion: extend edges by 1-3 random steps
- Hole carving: identify sardine clusters, carve rectangular holes
- Lobe merging: if two lobes share an edge, consider merging them

## Implementation Notes
- Use std::map for O(log n) vertex lookup
- Probe budget: 30 probes per evaluation
- Time budget: ~2.0s per evaluation
- Total evaluations: 30 budget, aim to use 15-20
