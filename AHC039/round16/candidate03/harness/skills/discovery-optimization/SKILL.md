---
name: discovery-optimization
description: "Spatial clustering and rectangle optimization. Use KD-tree for efficient spatial queries, find dense mackerel clusters, build minimal bounding rectangles, hill climb edge positions with \u00b110..20 shifts, run 8-10 strategic restarts."
---

# Spatial Clustering Polygon Strategy

## Phase 1: Exact Input Analysis
- Parse all fish coordinates precisely (no grid approximation)
- Build KD-tree for O(log N) spatial queries
- Identify all mackerel and sardine positions

## Phase 2: Cluster Detection
- Group mackerels by spatial proximity (distance threshold ~2000)
- For each cluster, compute:
  * Bounding rectangle
  * Exact count of mackerels inside
  * Exact count of sardines inside (using KD-tree query)
  * Score = M - S

## Phase 3: Rectangle Construction
- For each cluster, build minimal axis-aligned rectangle
- Expand rectangle slightly (±50, ±100) if it captures more mackerels
- Compute score for each variant

## Phase 4: Combination Strategy
- If two rectangles are close, consider merging them
- Merged polygon = union of both rectangles (may need vertex merging)
- Score combined polygon, compare to separate

## Phase 5: Hill Climbing
- For each rectangle: try edge shifts ±10, ±20, ±30 units
- Use KD-tree to count fish in shifted rectangle (O(N) with spatial index)
- Keep best shift per edge
- Repeat up to 100 iterations or until no improvement

## Phase 6: Strategic Restarts
- Run 8-10 restarts
- Each: 
  * Randomly sample 30-50 mackerel positions
  * Build bounding rectangle
  * Hill climb from there
- Track best polygon across all restarts

## Phase 7: Output
- Format as: m (vertex count) followed by vertex coordinates
- Ensure perimeter ≤ 400,000 and all coords in [0,100000]
