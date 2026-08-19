---
name: discovery-optimization
description: "Geometric polygon optimization: Construct axis-aligned polygons to maximize mackerels minus sardines. Use probe_solution to rank variants cheaply, then confirm with evaluate_solution. Follow the structured search method in system_prompt."
---

# Geometric Polygon Optimization

## Method
1. **Read task**: Maximize (mackerels - sardines + 1) with an orthogonal polygon.

2. **Use analyze_fish_geometry**: Call this tool ONCE at the start to get:
   - Total count of each fish type
   - Bounding boxes per type
   - Density estimates
   - Cluster information
   This informs your polygon design strategy.

3. **Design polygon strategy**:
   - If mackerels are clustered: enclose the cluster tightly
   - If mackerels are spread: use a larger bounding box with strategic cutouts
   - Place sardine-exclusion zones by indenting the polygon edges

4. **Iterate with probing**:
   - Generate 3-5 variants with different parameters (bounds, cutout positions)
   - Probe each (fast, uses probe budget)
   - Rank by probe score
   - Full-eval only the top 1-2 variants

5. **Refinement phases**:
   - Phase 1: Baseline (simple bounding box around mackerels)
   - Phase 2: Cutouts (add indentations around sardine clusters)
   - Phase 3: Expansion (extend where sardines are sparse)
   - Phase 4: Local optimization (small edge adjustments)

6. **Handle failures**:
   - If validity=0: Fix the constraint violation (too many vertices, too long perimeter, etc.)
   - If score decreases: Revert to previous approach, try a genuinely different strategy

## Tool calling order
1. analyze_fish_geometry (once)
2. edit_solution (hypothesis)
3. probe_solution (rank 3-5 variants)
4. evaluate_solution (best variant only)
5. Repeat until no improvement or budget exhausted

## Key constraints to respect
- Perimeter <= 400,000
- Vertices <= 1,000
- Coordinates 0-100,000
- No self-intersection
- Must output a valid orthogonal polygon
