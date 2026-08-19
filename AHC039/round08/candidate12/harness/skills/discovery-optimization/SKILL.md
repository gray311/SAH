---
name: discovery-optimization
description: "Global coordinate-space polygon optimization. Build comprehensive spatial index, perform greedy rectangle expansion with perimeter awareness, combine multiple shapes, and use time-bounded multi-strategy search to find optimal polygon."
---

# Global Coordinate-Space Polygon Optimization

## Overview: Unlike local cluster search, we explore the ENTIRE coordinate space systematically.

### Phase 1: Build Comprehensive Spatial Index
- Grid: 500x500 cells over [0,100000]x[0,100000] (cell_size=200)
- For each cell: count mackerels (M), sardines (S), store positions
- Compute score density = M / max(1, S + 0.1)
- Identify high-density regions (density > 1.0, 1.5, 2.0, ... up to 10%)
- For each region, compute initial bounding box

### Phase 2: Greedy Rectangle Expansion
For each high-density region:
1. Start with region's bounding box (minX, minY, maxX, maxY)
2. For each edge, try expanding outward by d = 50, 100, 150, 200, ... units
3. After each expansion, compute score using grid query
4. Track expansion: delta_score / delta_perimeter
5. Continue while delta_score / delta_perimeter > 0.3 and perimeter < 400000
6. Also try contractions (shrink edges) to exclude nearby sardines
7. Keep best rectangle for this region

### Phase 3: Multi-Shape Combination
1. Take top 3 rectangles from different high-density regions
2. Compute their union as a polygon (may have up to 12 vertices)
3. Verify validity: no self-intersection, perimeter ≤ 400000
4. Score the combined shape
5. If score > best single rectangle, use combination; else use best single

### Phase 4: Hill Climbing with Boundary Smoothing
For each edge of best polygon:
1. Try shifting edge by ±1, ±2, ..., ±50 units
2. Verify validity (no self-intersection, valid perimeter)
3. Compute score after shift
4. Keep shifts that improve score
5. Repeat with step sizes: 50 → 20 → 10 units (3 rounds)

### Phase 5: Multi-Strategy Time-Bounded Search
Strategy A: Global expansion (10 random seeds, 0.4s each)
Strategy B: Contraction-focused (exclude sardines first, 0.3s)
Strategy C: Corner-focused (target high-density corners, 0.3s)
Strategy D: Perimeter-minimization (find minimal perimeter for target score, 0.3s)

Output best valid polygon across all strategies.

### Implementation Notes
- Use 2D grid for O(1) rectangle queries
- Parallelize strategy searches within time budget
- Use deterministic seeds for reproducibility within each strategy
- Validate all polygons: axis-aligned, no self-intersection, perimeter ≤ 400000, vertices ≤ 1000
