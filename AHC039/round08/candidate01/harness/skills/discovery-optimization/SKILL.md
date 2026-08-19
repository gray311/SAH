---
name: discovery-optimization
description: "Optimize polygon using boundary-based exclusion analysis. Identify edges where sardines can be excluded with minimal mackerel loss. Use exclusion map to guide notch placement and L-shape cuts. Multi-scale refinement. 10 restarts."
---

# Boundary-Based Exclusion Polygon Optimization

## Core Insight: Sardines on polygon edges hurt score more than mackerels inside help
The optimal polygon often excludes sardines by cutting notches at edges rather than making large boundary cuts.

### Phase 1: Build Exclusion Map
- Create a spatial grid (cell_size=200)
- For each cell on grid boundaries, compute:
  - mackerels_on_edge: mackerels whose bounding box edge passes through this cell
  - sardines_on_edge: sardines whose bounding box edge passes through this cell
  - exclusion_ratio = sardines_on_edge / (sardines_on_edge + mackerels_on_edge)
- Mark high-exclusion cells (ratio > 0.5) as "cut zones"

### Phase 2: Edge Notch Generation
For each edge of the mackerel bounding box:
1. Find all sardines within 200 units of this edge
2. Sort sardines by distance from edge (closest first)
3. For each sardine, compute notch depth that excludes it but minimizes mackerel loss:
   - Notch depth = sardine_distance + 50 to 150
   - Estimate mackerel loss by counting mackerels in the notch rectangle
   - Score = (sardines_excluded) - (mackerels_lost)
4. Select top 3 notches per edge
5. Generate polygon with these notches applied

### Phase 3: Corner L-Shape Optimization
For each of 4 corners:
1. Check if opposite corner has high sardine density
2. If yes, generate L-shape that keeps current corner, cuts off opposite
3. Score each L-shape using grid query
4. Keep best L-shapes (up to 2 per corner)

### Phase 4: Multi-Scale Refinement
1. Start with coarse 500x500 grid
2. For polygons scoring > baseline, refine with 100x100 grid in the polygon region
3. Apply edge shifts of ±5, ±10, ±20 units guided by exclusion map
4. Keep improvements

### Phase 5: Multiple Restarts
- Run 10 restarts with different random perturbations
- Each restart: 700ms time budget
- Track best polygon across all runs

### C++ Implementation Notes
- Use fixed-size arrays for grids (fast O(1) access)
- Pre-compute exclusion map in O(N)
- Edge notch scoring: O(num_edges * num_sardines_near_edge)
- Total time per evaluation: < 0.8s
