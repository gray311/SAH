---
name: discovery-optimization
description: "Bounded iterative search with coarse-grained bounding box heuristic. Run 5-8 iterations, each generating 3-5 variants via expansion/contraction/vertex modification. Score variants with 10x10 coarse grid heuristic before full evaluation."
---

# Bounded Iterative Search with Coarse-Grained Heuristic

## Core Strategy

Instead of complex grid-based corridor expansion, use a simple but effective iterative search:

### Step 1: Initialize Base Polygon
- Compute bounding box of all fish points
- Create a minimal 4-vertex rectangle (top-left, top-right, bottom-right, bottom-left)
- This ensures we start with a valid polygon that captures all fish

### Step 2: Bounded Iterative Search Loop
- Set max_iterations = 6, time_per_iteration = 0.25s (total ~1.5s)
- For each iteration:
  * Generate 3-5 variant polygons:
    - **Expand**: Extend one edge outward by 50-500 units in cardinal direction
    - **Contract**: Shrink one edge inward by 10-100 units  
    - **Corner Add**: Insert 1-2 new vertices to create an L-shape or convex extension
    - **Edge Shift**: Slightly shift an existing edge by ±5, ±10 units
  * Score each variant using COARSE-GRANULARITY HEURISTIC:
    - Divide the search space into 10x10 coarse grid (each cell is 10000x10000 units)
    - For each polygon, estimate M-S by:
      1. For each grid cell, count how many fish points fall within it (use KD-tree or simple iteration)
      2. Estimate score ≈ sum(cell_M - cell_S) weighted by cell coverage ratio
      3. This takes O(poly_vertices * num_fish) but with coarse grid, average case is fast
  * Keep top 2 variants that have heuristic_score > current_best_heuristic AND valid geometry
  * Replace current polygon with best variant

### Step 3: Multiple Independent Searches
- Run 3 independent searches with different random seeds
- Track best polygon across all searches

### Step 4: Final Validation
- Ensure output meets all constraints:
  * 4 <= vertices <= 1000
  * Perimeter <= 400,000
  * All coords in [0, 100000]
  * No self-intersection (check edge overlaps)

## Why This Works

- **Simple mutations**: Easy for the LLM to generate valid variants
- **Coarse heuristic**: Fast O(1) relative to full evaluation, allows exploring many variants
- **Bounded iterations**: Guarantees staying under 2.0s
- **Multiple seeds**: Increases diversity of search paths
