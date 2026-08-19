---
name: discovery-optimization
description: "Aggressive local search with targeted expansion. Start from minimal polygon, mutate edges with \u00b15..20 shifts and vertex operations, expand toward mackerel-rich regions, run 3-5 focused searches, output best result."
---

# Aggressive Local Search for Polygon Optimization

## Phase 1: Initialization
- Start with a minimal valid polygon (e.g., a small rectangle at corner [0,0])
- Alternatively, start from a bounding box of random fish cluster

## Phase 2: Edge Mutation and Hill Climbing
For each edge of the polygon:
- Try shifting the endpoint by ±5, ±10, ±15, ±20 units (parallel to edge direction)
- Try adding a new vertex by splitting the edge at regular intervals (every 100-500 units)
- Try merging collinear adjacent edges (removing redundant vertices)
- For each mutation, estimate score change using grid-based lookup or quick estimate
- Apply all mutations that improve the score

## Phase 3: Targeted Expansion
- Compute a grid of fish density (mackerel vs sardine)
- Identify "rich" cells: high mackerel count, low sardine count
- Extend polygon edges toward these cells in cardinal directions
- Limit extension: stop when sardine penalty outweighs mackerel gain

## Phase 4: Multiple Focused Runs
- Run 3-5 independent searches with different seed mutations:
  * Randomly perturb initial rectangle coordinates
  * Different starting orientations
- Each search: aggressive hill climbing as in Phase 2-3
- Track best polygon across all runs

## Phase 5: Final Validation
- Ensure 4 <= vertices <= 1000
- All coordinates in [0,100000]
- No self-intersection (cross-product check for consecutive and non-adjacent edges)
- Perimeter <= 400,000

## Implementation Notes
- Use O(1) grid lookup for fast scoring during hill climbing
- Limit total operations per search to ~100,000 to stay under 2.0s
- Use std::random_device for seed generation in multiple runs
- Validate all outputs before printing
