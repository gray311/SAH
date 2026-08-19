---
name: discovery-optimization
description: "Optimize C++ polygon construction using cluster-based search. Find dense mackerel regions, generate indented/stepped polygons around them, and hill climb edges. Use spatial grid for fast fish counting."
---

# Cluster-Based Polygon Optimization

## Strategy: 1. Cluster Analysis → 2. Pattern Generation → 3. Hill Climb

### Phase 1: Identify High-Value Clusters
- Build a 200x200 cell grid over [0, 100000] x [0, 100000]
- For each cell, count mackerels (M) and sardines (S)
- Compute score = M - S for each cell
- Find top 10 cells with highest score (mackerel-rich, sardine-poor)
- Expand each top cell into a 500x500 region and recompute
- These are your "seed clusters"

### Phase 2: Generate Candidate Polygons
For each seed cluster, generate 3 patterns:

**Pattern A: Tight Bounding Box**
- Compute minX, maxX, minY, maxY of all mackerels in cluster
- Output this rectangle (4 vertices)
- Score: count mackerels inside - count sardines inside

**Pattern B: Indented Box (Exclude Nearby Sardines)**
- Start with Pattern A's bounding box
- For each sardine within 300 units of the box edge:
  - Indent that edge inward by 50-100 units toward the sardine
  - This excludes the sardine while keeping most mackerels
- Output the modified polygon (6-8 vertices)

**Pattern C: Stepped L-Shape (Corner Capture)**
- Identify the corner of the bounding box farthest from sardines
- Create an L-shaped polygon: keep that corner intact, cut off the opposite side
- This captures dense corner mackerel while avoiding edge sardines
- Output (6 vertices)

### Phase 3: Hill Climbing Refinement
For each candidate from Phase 2:
- For each edge (4-8 edges):
  - Try shifting the edge inward by ±1, ±2, ..., ±20 units
  - After each shift, recompute score using grid query
  - Keep the shift that improves score
- Repeat up to 3 refinement rounds
- Output the refined polygon

### Phase 4: Multiple Random Restarts
- Run Phases 1-3 with 5 different random seeds (perturb cluster selection)
- Track the best polygon across all runs
- Output that single best polygon

## C++ Implementation Notes
- Use a fixed-size array for the 200x200 grid (fast access)
- Pre-compute all grid cell scores in O(N) at startup
- Rectangle query = sum of grid cells covering the rectangle
- Total time per evaluation: < 0.5s with efficient grid operations
