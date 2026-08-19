You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL SEARCH STRATEGY: Multi-scale sliding window with polygon merging

PHASE 1: Fine-grained clustering
- Build a 50x50 cell grid (2000x2000 cells) over [0,100000] x [0,100000]
- For each cell, count mackerels (M) and sardines (S)
- Find top 50 cells with highest (M - S) score
- Expand each top cell into a 500x500 region and recompute M, S

PHASE 2: Per-cluster polygon generation
For each of the top 50 clusters:
- Compute bounding box of ONLY mackerels in the cluster (ignore sardine positions for box)
- Generate 4 variants:
  * Variant 0: Tight bounding box of mackerels
  * Variant 1: Cut top-right corner by 100 units to exclude corner sardines
  * Variant 2: Cut bottom-left corner by 100 units
  * Variant 3: Cut both opposite corners to create a cross shape
- For each variant, score using grid query (M_inside - S_inside + 1)

PHASE 3: Polygon merging
- Start with an empty polygon
- For each cluster's best variant, try to merge it with the current polygon:
  * If non-overlapping: add as new vertex chain
  * If partially overlapping: compute union of the two axis-aligned rectangles
  * If one contains the other: keep the larger one
- After processing all 50 clusters, simplify the merged polygon (remove collinear vertices)

PHASE 4: Edge refinement (per-cluster, not global)
- For each final edge in the merged polygon:
  * Try moving it inward by 5, 10, 15, 20, 25, 30 units
  * For each move, recompute score using grid query
  * Keep the move that improves score
- Repeat 2 refinement rounds

PHASE 5: Random restarts
- Run Phases 1-4 with 10 different random seeds (perturb cluster selection by ±10 in rank)
- Track the best polygon across all runs

Search MUST use the full 2.0s time budget. Output the single best valid polygon.
