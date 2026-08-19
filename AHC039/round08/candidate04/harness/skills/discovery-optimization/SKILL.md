---
name: discovery-optimization
description: "Optimize C++ polygon construction using sardine-aware search. Build fine 500x500 grid, identify mackerel clusters and nearby sardine clusters, then carve sardines out with notch-shaped indents. Hill climb edge shifts that maximize (mackerels - sardines)."
---

# Sardine-Aware Polygon Optimization

## Strategy: 1. Fine Grid → 2. Cluster Detection → 3. Notch Carving → 4. Hill Climb

### Phase 1: Fine-Grained Spatial Analysis
- Build 500x500 grid (cell_size=200) over [0,100000]x[0,100000]
- For each cell, count mackerels (M) and sardines (S)
- Identify top 15 mackerel-dense cells AND top 15 sardine-dense cells separately

### Phase 2: Sardine-Aware Polygon Generation
For each top mackerel cluster:

**Step A: Base Bounding Box**
- Compute minX, maxX, minY, maxY of all mackerels in cluster
- Create initial rectangle (4 vertices)

**Step B: Detect Nearby Sardines**
- For each sardine cell in top 15, check if it overlaps or is adjacent to the bounding box
- Mark sardine regions that need exclusion

**Step C: Carve Out Sardines with Notches**
For each sardine to exclude:
- If sardine is on an edge: indent that edge inward by 50-150 units around the sardine's position
- This creates a "notch" - the polygon goes around the sardine
- A sardine notch adds 2 vertices per notch (in and out)
- Output polygon with 8-16 vertices (4 base + 2 per notch)

**Step D: Score the Notched Polygon**
- Count mackerels inside the notched polygon
- Count sardines inside (should be much lower)
- Compute score = M - S + 1

### Phase 3: Sophisticated Hill Climbing
For each notched polygon candidate:
- For each edge (8-16 edges):
  - Try shifting edge inward by ±5, ±10, ±20, ±30, ±40, ±50 units
  - After each shift, recompute score using grid query
  - Keep shifts that: increase M OR decrease S (mackerel sacrifice is OK if sardine reduction is large)
  - Priority: reduce sardines > increase mackerels
- Repeat up to 2 refinement rounds
- Track best polygon

### Phase 4: Multiple Random Restarts
- Run Phases 1-3 with 8 different random seeds (perturb cluster selection)
- Each seed uses different mackerel clusters and different notch parameters
- Track the best polygon across all runs
- Output that single best polygon

## C++ Implementation Notes
- Use 500x500 grid for O(1) rectangle queries (much finer than 200x200)
- Pre-compute all grid cell scores in O(N) at startup
- Sardine exclusion: for each sardine, find which edge(s) to notch and by how much
- Notch creation: replace a straight edge with an L-shaped indentation
- Total time per evaluation: < 1.5s with efficient grid operations and pruning
