---
name: discovery-optimization
description: "Seed-based local search with simulated annealing. Start from mackerel cluster bounding box, apply multi-objective hill climbing with occasional worsening moves (simulated annealing), add lobe expansions for disconnected clusters, 8 restarts."
---

# Seed-Based Local Search with Simulated Annealing

## Phase 1: Initial Polygon Construction

- Compute centroid of all mackerel points
- Group mackerels by a 500x500 grid and find the top 10 cells by mackerel density (mackerels/cell_area)
- Build a bounding rectangle around these top cells
- Ensure: all coords in [0,100000], perimeter <= 400,000, 4-1000 vertices

## Phase 2: Multi-Objective Simulated Annealing Hill Climbing

For 5 refinement rounds:

For each edge of the polygon:
- Try shifts in x direction: ±10, ±20, ±30
- Try shifts in y direction: ±10, ±20, ±30
- For each shifted edge, create a new polygon candidate
- Score each candidate using KD-tree based counting (exact score, not approximation)
- Compute delta_score = new_score - current_score

Acceptance criteria:
- If delta_score > 0: always accept
- If delta_score <= 0: accept with probability exp(-delta_score / T)
  where T starts at 50 and multiplies by 0.95 after each edge trial

Keep the best polygon after all edge trials

## Phase 3: Iterated Restarts

- Run 8 restarts with different random seeds
- Each restart:
  * Perturb initial rectangle corners by random amount in [-200, +200]
  * Apply simulated annealing hill climbing
  * Track the best polygon across all restarts

## Phase 4: Lobe Expansion for Disconnected Clusters

- After hill climbing, identify mackerel clusters that are outside the current polygon
- For each cluster (group of mackerels within 1000 distance of each other):
  * Build a small rectangle around the cluster
  * If adding this rectangle (union with current polygon) improves the score AND keeps perimeter <= 400,000, apply it
  * Check for self-intersection after each addition

## Phase 5: Final Validation

- Output exactly: m (number of vertices) then m lines of "x y" coordinates
- Ensure: 4 <= m <= 1000, all coords in [0,100000], no self-intersection, perimeter <= 400,000
- Use seed's KVH validator for self-intersection check

## Key Differences from Seed

- Uses simulated annealing to escape local optima (seed uses greedy hill climbing only)
- Starts from data-driven initial polygon (seed uses random rectangles)
- Adds lobe expansion for disconnected clusters
- More restarts with corner perturbation
