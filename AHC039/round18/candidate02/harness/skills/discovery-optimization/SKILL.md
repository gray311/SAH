---
name: discovery-optimization
description: "Start from seed [[0,0],[200,0],[200,200],[0,200]], use probe_solution to test expansions in all 4 directions up to 500 units.\nFor each direction, create 3-5 candidate expansions (different sizes), probe each, keep best.\nFull evaluate top 1-2 candidates. Hill climb with edge shifts if needed. Run 5-8 restarts with different seed sizes."
---

# Bidirectional Polygon Expansion Strategy

## Phase 1: Base Seed Analysis
Start with seed polygon P_seed = [[0,0],[200,0],[200,200],[0,200]].
This captures a 200x200 area. We need to expand it to capture more mackerels while avoiding sardines.

## Phase 2: Directional Expansion with Probing

For each cardinal direction (N,S,E,W):
1. Create candidate expansions: extend by d units in that direction, for d in [100, 200, 300, 400, 500]
2. For each candidate, use probe_solution to get approximate score
3. Record (direction, extension_size, probe_score)

**Bidirectional strategy**: When expanding North, also check if we should expand South from some interior edge.

## Phase 3: Combined Polygon Construction

From top 4-8 expanded candidates (by probe score):
1. Create the polygon: merge expansion from original seed
2. Example: If expanded N by 300 and E by 200:
   Original seed: [[0,0],[200,0],[200,200],[0,200]]
   After N expansion (300): [[0,200],[200,200],[200,500],[0,500]] + upper part connected to seed
   Actually: Create single polygon [[0,0],[200,0],[200,500],[0,500],[0,0]] for N=300 expansion

## Phase 4: Hill Climbing

For each candidate polygon:
- For each edge (up to 8 vertices for axis-aligned rectangle):
  * Try expanding this edge by ±20, ±50, ±100 units
  * Use probe_solution to check score
  * Keep best expansion

## Phase 5: Multiple Restarts

- Run 5-8 restarts with different strategies:
  * Start with seed expanded to different sizes (200x200, 400x400, 600x600)
  * Expand in different direction combinations (N only, E only, N+E, etc.)
- Track best polygon across all restarts

## Phase 6: Final Validation

- Ensure 4 <= vertices <= 1000
- Ensure coordinates in [0, 100000]
- Ensure perimeter <= 400,000
- Use KVH validator to check no self-intersection

## Key Metrics

- Probe 10-20 variants before any full evaluation
- Full evaluate only the best 1-2 candidates
- Use remaining time for hill climbing on best candidates
