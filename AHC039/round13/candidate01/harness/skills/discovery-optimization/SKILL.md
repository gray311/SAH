---
name: discovery-optimization
description: "Cluster-based polygon optimization. Use KD-tree to efficiently count fish in rectangles, identify dense clusters, generate bounding-box polygons, probe-screen candidates, fine-tune vertices, run 25 restarts."
---

# Cluster-Based Polygon Construction Strategy

## Phase 1: Data Loading and KD-Tree Construction
- Parse input: first N lines are mackerels (type=1), next N lines are sardines (type=-1)
- Build KD-tree with all 10,000 fish points for O(log N) rectangle queries
- Use the existing KDNode structure but ensure it's properly populated

## Phase 2: Cluster Discovery
- Sample 50 random points from KD-tree
- For each sample point, find its cluster: all fish within 5000 pixels
- Cluster scoring: mackerel_count - sardine_count
- Select top 10 clusters by score (even if negative, they might become positive with better polygon)

## Phase 3: Bounding Box and Polygon Generation
- For each cluster, compute tight axis-aligned bounding box [min_x, max_x, min_y, max_y]
- Generate polygon candidates:
  * Original bounding box rectangle
  * 20 shifted rectangles: shift left/right/up/down by 10, 20, 30, 40 pixels
  * 10 rectangles with adjusted aspect ratios (maintain similar area)
- Total candidates per cluster: ~31

## Phase 4: Probe-Based Screening (Critical)
- For each candidate polygon, use probe_solution if available for fast approximate scoring
- If probe not available: compute count_fish_in_rect via KD-tree rectangle query (much cheaper than full eval)
- Use threshold: keep only candidates with estimated score > 1.5
- Typical reduction: from 300+ candidates to 20-50

## Phase 5: Fine-Tuning
- For each surviving candidate:
  * Extract all unique x and y coordinates from vertices
  * For each vertex, try shifts of ±5, ±10, ±15 pixels
  * Evaluate each shift using probe or KD-tree query
  * Keep best shift for each vertex
  * Repeat up to 3 rounds of refinement

## Phase 6: Multiple Restarts
- Run 25 independent restarts with different random seeds
- Each restart uses different random sampling for cluster discovery
- Track best polygon across all restarts

## Phase 7: Output
- Validate polygon constraints: 4-1000 vertices, perimeter ≤ 400,000, integer coords in [0,100000]
- Output format: vertex_count followed by "x y" for each vertex

## Implementation Notes
- KD-tree rectangle query is O(k + log N) where k is fish in rectangle - very fast
- Probe budget: 30 probes per full evaluation - use them to screen many candidates
- Total time budget: 2.0s - structure work to complete within this
- Use static grid fallback if KD-tree proves too complex
