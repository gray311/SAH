---
name: discovery-optimization
description: "Rectangle-based cluster optimization. Build 500x500 sparse grid, find mackerel-dense cells, create bounding box candidates expanded 200 units each way, evaluate top 50, local dimension search with \u00b150..150 perturbations, 25 restarts."
---

# Rectangle-Based Cluster Optimization Strategy

## Phase 1: Sparse Grid Construction
- Use 500x500 grid with cell_size=200 (covers 0-100000)
- For each cell, count mackerels (M) and sardines (S) from input
- Compute cell score = M - S
- Store all mackerel positions for rectangle construction

## Phase 2: Candidate Rectangle Generation
For each mackerel cell with M > 0:
- Create a base rectangle covering that cell
- Expand each side by 200 units (bounded by [0,100000])
- Estimate: M_count using grid cells inside rectangle, S_count similarly
- Compute heuristic score = (estimated_M - estimated_S) / perimeter
- Add to candidate pool

## Phase 3: Candidate Selection
- Sort candidates by heuristic score (descending)
- Pick top 50 candidates for full evaluation

## Phase 4: Full Evaluation and Refinement
For each of top 50 candidates:
- Count actual mackerels and sardines inside rectangle (O(N) scan)
- Compute actual score = M - S + 1
- Try dimension perturbations: expand/contract each side by ±50, ±100, ±150
  * Keep perturbation that improves actual score
  * Maintain bounds [0,100000] and perimeter <= 400,000
- Repeat refinement up to 3 rounds

## Phase 5: Multiple Restarts
- Run 25 restarts with different random seeds
- Each restart: 
  * Pick 10-15 random mackerel positions
  * Build rectangle candidates from each (200-unit expansion)
  * Evaluate top 50 candidates with refinement
- Track best rectangle across all restarts

## Phase 6: Output
- Output best rectangle as 4 vertices in order (e.g., bottom-left, bottom-right, top-right, top-left)
- Ensure valid format: 4 <= vertices <= 1000, integer coords, axis-aligned

## C++ Implementation Notes
- Use fixed-size 500x500 grid for O(1) cell access
- O(N) scan for rectangle evaluation (N=10000 fish)
- Total time per evaluation: < 2.0s with efficient operations
- Use std::random_device for seed generation
- Rectangles are self-validating (no intersection checks needed)
