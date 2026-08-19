---
name: discovery-optimization
description: "Local cluster-based polygon construction. Detect mackerel-dense cells (density > 2.0), build tight bounding box polygons around clusters, fine-grained edge tuning with \u00b11..5 shifts, 5-round refinement, iterative mutation loop (50 iterations), try separate and combined cluster strategies."
---

# Local Cluster-Based Polygon Optimization

## Phase 1: Cluster Detection

- Read fish coordinates from input
- Build spatial hash grid with cell_size=100 (covers 100000 range with 1000x1000 cells)
- For each cell, count mackerels (M) and sardines (S)
- Compute density = M / S (if S > 0, else infinity)
- Identify "high-density" cells: density > 2.0 AND M >= 5

## Phase 2: Tight Polygon Construction

For each high-density cluster:
- Find the minimal axis-aligned bounding box
- Convert to polygon vertices (4 vertices for rectangle)
- If cluster spans multiple cells, consider slightly larger box to include edge fish

## Phase 3: Fine-Grained Edge Tuning

For each edge (up to 1000 vertices):
- Try shifts: ±1, ±2, ±3, ±4, ±5 units in both perpendicular directions
- For each candidate edge position:
  * Count mackerels and sardines inside the modified polygon (using point-in-polygon)
  * Compute score = M - S
- Keep the shift that maximizes score

## Phase 4: Iterative Refinement (5 Rounds)

Round 1: step_size = 5
Round 2: step_size = 3
Round 3: step_size = 1
Round 4: step_size = 0.5 (round to nearest integer)
Round 5: step_size = 0.25 (round to nearest integer)

Each round:
- For each edge, try shifts of ±step_size
- Keep best modification

## Phase 5: Iterative Mutation Loop

For up to 50 iterations:
- Type A (edge shift): Pick random edge, try ±1, ±2, ±3, ±4 shifts perpendicular
- Type B (vertex add): Pick random edge midpoint, add new vertex offset by ±1, ±2 in both directions
- Type C (vertex remove): If polygon has > 6 vertices, try removing a vertex (merge edges)
- Evaluate each mutation using local fish counting (spatial index for O(1))
- Apply best mutation if it improves score
- Break if no improvement in 3 consecutive iterations

## Phase 6: Multi-Cluster Strategy

- Build separate polygon for each top 5 clusters
- For each pair of adjacent clusters, try connecting with minimal corridor
- Compare all options, output best

## Phase 7: Validation

- Ensure 4 <= vertices <= 1000
- Check integer coordinates in [0, 100000]
- Verify no self-intersection (simple edge-edge intersection test)
- Verify perimeter <= 400,000

## Implementation Notes

- Use spatial hash for O(1) fish counting in local regions
- Pre-filter fish by checking if inside polygon using ray casting
- Keep total runtime < 2.0 seconds per evaluation
- Output format: m (vertices) then m lines of "x y"
