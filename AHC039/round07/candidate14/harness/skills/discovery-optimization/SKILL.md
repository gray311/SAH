---
name: discovery-optimization
description: "Optimize C++ polygon-constructing code for NP-hard fish-capture. Use PROBE-FIRST strategy:\ngenerate many polygon candidates, quickly rank with 5% sampling (analyze_polygon), then\nconfirm top candidates with full evaluation. Implement KD-tree/grid spatial indexing for\nfast fish counting. Use hill-climbing with edge perturbations to refine best polygon.\nTime budget 2s: setup 0.1s, probe 0.8s, refine 0.6s, verify 0.5s."
---

# Fish Capture Polygon Optimization with Probe-First Search

## Problem
- N=5000 mackerels (type=1), N=5000 sardines (type=-1)
- Maximize: mackerels_in - sardines_in + 1
- Polygon: axis-aligned, max 1000 vertices, perimeter <= 400000
- Time: 2s per evaluation

## Proven Strategy: Probe-First Search with Spatial Indexing

### Phase 1: Build Spatial Index (0.1s)
- Construct KD-tree or uniform grid over all fish
- Grid cell size 1000-2000 units for balanced queries
- Enables O(1) approximate fish count in any rectangle

### Phase 2: Generate Candidate Polygons (0.5s)
- Base: Bounding box of all mackerels
- Variants: 
  * 100+ random rectangles within coordinate bounds
  * L-shapes: capture corners around mackerel clusters
  * Stepped polygons: staircase patterns following mackerel density
  * Sardine-exclusion: indent edges near sardine concentrations

### Phase 3: Probe Top Candidates (0.8s)
- For each candidate, call analyze_polygon (5% fish sample)
- Track probe scores: mackerels_probe - sardines_probe + 1
- Keep top 3-5 candidates by probe score

### Phase 4: Full Evaluation & Refinement (0.6s)
- Evaluate the best probe candidate with evaluate_solution
- If score > current best, refine:
  * Perturb each edge by 1 to 50 units (axis-aligned)
  * Re-probe all variants, keep improvements
  * Repeat 5-10 refinement iterations

### Phase 5: Multi-Restart Search
- Run 3-5 independent searches from different starting polygons
- Track global best across all restarts
- Merge promising local optima if they share boundary regions

### C++ Implementation Checklist
- Build KD-tree on all 10000 fish at startup
- Implement analyze_polygon(ctx, sample_frac=0.05)
- Implement generate_candidates() returning 50-200 polygon variants
- Implement refine_polygon(best_poly, max_delta=50, iterations=10)
- Main loop: generate -> probe -> eval top -> refine -> repeat until timeout

### Critical Pitfalls
- NEVER call evaluate_solution more than once per refinement cycle
- Always output VALID polygon (check perimeter, non-self-intersection)
- Use seed timer to enforce strict time budget
- 5% sampling is statistically sufficient for relative ranking
- Sardines hurt score significantly - prioritize exclusion over mackerel inclusion
