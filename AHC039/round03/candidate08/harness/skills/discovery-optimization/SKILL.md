---
name: discovery-optimization
description: "Optimize axis-aligned polygon construction for fish scoring. Use probe-guided search,\nboundary expansion, and efficient data structures. Maximize mackerel-sardine score within time budget."
---

# Polygon Optimization Playbook

## Objective
Construct an axis-aligned polygon to maximize (mackerel_count - sardine_count + 1).

## Search Strategy
1. INITIAL CONSTRUCTION: Start with minimal 4-vertex rectangle.

2. BOUNDARY EXPANSION: Add vertices along boundary lines. For each side:
   - Generate candidate x-coordinates from all mackerel/sardine x-coordinates
   - Generate candidate y-coordinates from all mackerel/sardine y-coordinates
   - Try extending edges to these coordinates, checking perimeter constraint

3. EDGE POSITION OPTIMIZATION: For each horizontal/vertical edge:
   - Binary search or step-based search over the relevant coordinate range
   - Track which x-range (or y-range) each edge covers
   - Calculate marginal gain: mackerels added minus sardines added

4. PROBE-GUIDED SEARCH (CRITICAL):
   - Generate 5 to 10 polygon variants from your current search state
   - Call probe_solution on each to get approximate scores
   - Select top 1 to 2 variants by probe score
   - Call evaluate_solution ONLY on the best one
   - This maximizes your chance of finding the optimal solution within budget

5. DATA STRUCTURES:
   - Use coordinate compression: collect all x and y from fish, sort and unique
   - Build 2D grid with cell counts or use sorted containers per coordinate
   - For point-in-polygon: ray-casting or edge-crossing count
   - Maintain active edges list to quickly recompute perimeter

6. TIME BUDGET: 1.95 seconds per evaluation. Your search loop must:
   - Use while(tick() < 1.945) to track time
   - Return immediately if time exceeds limit
   - Include early termination if 10 consecutive iterations do not improve

7. VALIDATION CHECKS (before output):
   - vertices.size() in [4, 1000]
   - perimeter <= 400000
   - all coords in [0, 100000]
   - no self-intersection (adjacent edges meet at endpoints only)

## Typical Loop Structure
while timer elapsed() < 1.945:
    try_expanding in one direction
    generate 5 variants from current state
    call probe_solution on each variant
    select top 1 variant by probe score
    call evaluate_solution on the best variant only
    if full score improves, update best
    optimize edge positions using marginal gains

## Common Pitfalls
Do not use brute-force over all possible polygons.
Do not ignore the perimeter constraint (400000).
Do not call evaluate_solution too frequently; use probe_solution first.
Do not let search time exceed 1.95s.
Do not output invalid polygons; check all constraints.
