---
name: discovery-optimization
description: "Local search with probe-based ranking. Start from seed/rectangle, perturb vertices (\u00b11..50), rank with probe_solution, evaluate top 3, 10 restarts."
---

# Local Search with Probe-Based Ranking

## Core Strategy

Instead of building polygons from grid corridors, use iterative vertex perturbation:

### Phase 1: Initial Solution
- Use seed program's polygon OR create a simple axis-aligned rectangle
- Ensure validity: 4-1000 vertices, perimeter≤400000, coords in [0,100000]

### Phase 2: Vertex Perturbation
For each vertex:
- Try shifts: ±1, ±2, ±5, ±10, ±15, ±20, ±25, ±30, ±40, ±50 units
- In each axis-aligned direction (N/S/E/W)
- Generate candidate polygon (replace that vertex)
- Track all valid candidates

### Phase 3: Probe-Based Ranking
- Submit ALL candidates to probe_solution (up to 30 probes)
- Use approximate scores to rank candidates
- Probe is cheap (~10s) and separate budget

### Phase 4: Deep Evaluation
- Pick top 3 candidates by probe score
- Evaluate each fully with evaluate_solution
- Keep best

### Phase 5: Multi-Lobed Extension (if improving)
- If score improves, try adding vertices (split edges) or removing vertices (merge collinear)
- Create multi-lobed structures that wind through fish clusters
- Repeat perturbation from new base

### Phase 6: Multiple Restarts
- Run 10 restarts with different random seeds
- Each restart: perturb different vertices, different shift magnitudes
- Output best polygon across all restarts

## Implementation Notes
- Use efficient vertex mutation: O(V) per candidate where V≤1000
- Parallelize probe submissions if possible
- Cache probe results to avoid redundant calls
- Total time < 2.0s per evaluation
