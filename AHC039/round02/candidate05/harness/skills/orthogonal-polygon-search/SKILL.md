---
name: orthogonal-polygon-search
description: Build multiple orthogonal polygons inside C++ search loop. Use spatial indexing (grid/KD-tree) for fast point queries. Implement 3+ construction strategies - grid-sweep, rectangle-merge, and perimeter-constrained path-following. Validate each candidate with validate_polygon before evaluation. Budget - ~1.85s search, 10-20 full evals.
---

# Orthogonal Polygon Search Playbook

## Core Loop Structure
best_score = -1
best_polygon = []

time_remaining = 1.85
start_time = now()

while time_remaining > 0.05 and iterations < 100:
    # Phase 2: Construct
    polygon = construct_polygon(strategy=X, params=p)
    
    if polygon is null:
        try_next_strategy()
        continue
    
    # Fast perimeter filter
    pcheck = quick_perimeter_check(polygon.vertices)
    if pcheck.status == "over_budget":
        continue
    
    # Full validation
    vresult = validate_polygon(polygon.vertices)
    if not vresult.valid:
        continue
    
    # Phase 3: Evaluate top candidates
    if we have < 15 evals used:
        score = evaluate_solution()
        if score > best_score:
            best_score = score
            best_polygon = polygon
    
    # Phase 2.5: Probe-ranking (optional)
    if we have probes left and have > 5 valid polygons:
        rank_polygons_with_probes()
        only eval top 3
end loop

# Phase 4: Output best
return best_polygon

## Construction Strategies

### Strategy 1: Grid-Sweep from Centroid
1. Find centroid of all mackerels: cx = avg(x), cy = avg(y)
2. Place initial 4 vertices at (cx +/- dx, cy +/- dy) for some dx,dy
3. Expand in spiral pattern: each ring adds 4 edges
4. Snap vertices to integer grid points
5. Prune vertices that add sardines without enough mackerels

### Strategy 2: Bounding-Box + Hole Removal
1. Compute bounding box of all mackerels
2. If sardines inside, carve out orthogonal holes
3. Expand bounding box to include more mackerels if needed
4. Ensure perimeter <= 400000

### Strategy 3: Perimeter-Bound MST Path
1. Select ~300 mackerels with highest density
2. Build orthogonal path visiting them (Manhattan MST variant)
3. Close the loop ensuring no self-intersection
4. Fill interior and count mackerels/sardines

## Validation Checklist
- vertices >= 4 and <= 1000
- all vertices distinct
- each edge axis-aligned (dx=0 or dy=0)
- perimeter <= 400000 (use Manhattan sum for orthogonal)
- coords in [0, 100000]
- no self-intersection (non-adjacent edges do not share points)

## Timing Budget
- Grid building: O(N) with hash table
- Vertex construction: O(V^2) where V ~ 300-500 vertices
- Point-in-polygon: O(V) naive, O(log V) with KD-tree
- Aim for < 50ms per polygon construct
- Leave 0.5s for evaluation if needed
