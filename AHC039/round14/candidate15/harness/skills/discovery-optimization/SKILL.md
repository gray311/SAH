---
name: discovery-optimization
description: "Coordinate-based KD-tree spatial indexing, generate 15-20 polygon variants with edge expansions and vertex additions, rank via probe_solution, evaluate top 1-3 with full scoring."
---

# Coordinate-Based Polygon Optimization with Probe-Driven Search
## Phase 1: Spatial Indexing - Parse all 10000 fish points from input - Build KD-tree for efficient orthogonal range queries - Store points separately by type (mackerel=+1, sardine=-1)
## Phase 2: Polygon Generation Start from seed and generate diverse candidates:
### Base Rectangle Construction - Pick random x1<x2, y1<y2 within [0,100000] - Ensure perimeter <= 400,000 - Output 4 vertices
### Expansion Mutations For each base shape, apply mutations: - Edge expansion: extend each edge by k units (k∈[10,50,100,200]) - Vertex insertion: add points at (fish_x, fish_y) coordinates to create corners - Multi-lobed: split into 2-4 connected rectangles, joined at shared edges
### Diversity Mechanisms - Random vertex perturbations (±10% of coordinate) - Random rotation of construction order - Different starting seeds for each variant
## Phase 3: Probe-Based Ranking - For each evaluation (30 probes available): - Generate 15-20 unique polygon candidates - Use probe_solution for each (cheap, ~10s, separate budget) - Record approximate scores - Sort by probe score descending
## Phase 4: Full Evaluation - Pick top 1-3 candidates by probe score - Use evaluate_solution on each (exact scoring, consumes main budget) - Output the single best valid polygon
## Phase 5: Validation - Check: 4 <= vertices <= 1000 - Check: perimeter <= 400,000 - Check: all coords in [0,100000] - Check: no self-intersection (adjacent edges meet at endpoints, non-adjacent don't touch) - Only output valid polygons
## C++ Implementation Notes - Use KD-tree (std::vector + nth_element partitioning) for O(log N) queries - Point-in-polygon for axis-aligned: simple bounding box check + winding number - Rectangle score: sum of fish inside using range queries - Probe function: call ctx.probe() with candidate polygon vertices - Evaluation function: call ctx.evaluate() with candidate - With 30 probes, you can afford 15-20 candidates with cheap filtering
