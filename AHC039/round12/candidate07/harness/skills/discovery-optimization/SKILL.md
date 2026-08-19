---
name: discovery-optimization
description: "Direct geometric clustering. Identify mackerel clusters using coordinate analysis, build tight axis-aligned polygons around clusters, merge adjacent clusters strategically, aggressive hill climbing on vertices, multi-strategy ensemble with 8-10 approaches."
---

# Direct Geometric Clustering Strategy

## Phase 1: Fish Distribution Analysis
- Parse all fish coordinates directly (no grid abstraction)
- Compute 100x100 cell density map for hotspots
- Find bounding boxes for mackerel and sardine point clouds separately
- Identify high-density mackerel regions by clustering nearby points

## Phase 2: Cluster Formation
- Group mackerels into clusters using proximity (e.g., points within 2000 units)
- For each cluster, compute optimal axis-aligned bounding rectangle
- Score each rectangle: mackerels_inside - sardines_inside + 1
- Identify which rectangles have positive net score

## Phase 3: Polygon Assembly
- Start with highest-scoring single-cluster rectangle
- Try merging adjacent rectangles: connect them with minimal corridor
- For multiple clusters: build multi-lobed polygon that visits each cluster
- Consider ring/annulus patterns if mackerels form a surrounding region with sardines inside
- Ensure polygon validity: 4-1000 vertices, perimeter <= 400,000, no self-intersection

## Phase 4: Vertex Expansion Hill Climbing
For each candidate polygon:
- **Vertex Addition**: Try adding vertices at mackerel positions near polygon edges
- **Edge Expansion**: For each edge, try expanding outward by 5, 10, 20, 50, 100 units
- **Sardine Cutouts**: If polygon contains sardine clusters, try adding inward indentations
- **Corner Rounding**: Try slightly expanding corners to capture edge fish
- Repeat 2-3 rounds, keep best version

## Phase 5: Multi-Strategy Ensemble
Run 8-10 diverse strategies per evaluation:
1. Single-best-cluster rectangle
2. Top 3 cluster merge (minimal corridor)
4. All-positive-score clusters combined
5. Large enclosing box with sardine cutouts
6. Spiral pattern for concentric fish distributions
7. Band/strip following mackerel density gradient
8. Corner-focused expansion from seed region
9. Random perturbation of cluster centers
10. Greedy growth from highest-density point

Track best solution across all strategies, output single best polygon.

## C++ Implementation Notes
- Use O(N log N) or O(N²) clustering (N=5000 is manageable)
- Rectangle scoring: precompute fish counts in O(1) with 2D prefix sums
- Polygon validation: standard O(V²) edge intersection check
- Total time per eval: < 1.5s to allow buffer
- Use random seeds for strategy diversity
