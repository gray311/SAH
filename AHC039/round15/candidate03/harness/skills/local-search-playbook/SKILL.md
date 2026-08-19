---
name: local-search-playbook
description: Use vertex perturbation for local search. Perturb each vertex ±1..50 in 4 directions, rank with probe_solution, evaluate top 3, 10 restarts.
---

# Local Search with Probe-Based Ranking

## Phase 1: Initialization
- Start from seed program's polygon OR create simple 4-vertex rectangle
- Verify validity: 4≤vertices≤1000, perimeter≤400000, coords∈[0,100000]

## Phase 2: Generate Variants via Vertex Perturbation
For each vertex (x, y):
  For each direction: N(-1,0), S(1,0), E(0,1), W(0,-1)
    For shift in [1, 2, 5, 10, 15, 20, 25, 30, 40, 50]:
      new_vertex = (x + shift*dir_x, y + shift*dir_y)
      if new_vertex in [0,100000]²:
        candidate = copy(polygon) with vertex replaced
        if candidate valid (4≤m≤1000, perimeter≤400000):
          add to candidates list

## Phase 3: Probe-Based Ranking
- Submit all candidates to probe_solution (max 30 probes per evaluation)
- Use approximate scores to rank
- Probe budget: 30 separate from 30 real evaluations

## Phase 4: Deep Evaluation
- Pick top 3 candidates by probe score
- Call evaluate_solution on each
- Track best score across all 3

## Phase 5: Multi-Lobed Extension (optional)
If score improves:
  - Try adding vertex: split edge at midpoint or 1/3 point
  - Try removing vertex: merge adjacent edges if collinear
  - Create multi-lobed structures that wind through fish clusters
  - Repeat phases 2-4 from new base

## Phase 6: Multiple Restarts
- Run 10 restarts with different random seeds
- Vary: starting polygon, perturbation shifts, vertex selection order
- Output single best polygon

## Key Principles
- Probe first, evaluate sparingly (30 probes + 3 evals per restart)
- Small perturbations enable fine-grained search
- Multi-lobed structures can capture multiple fish clusters
