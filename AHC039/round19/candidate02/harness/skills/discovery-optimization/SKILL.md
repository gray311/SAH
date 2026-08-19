---
name: discovery-optimization
description: "Mackerel-focused clustering. Identify spatial clusters of mackerels (within 5000 distance),\nbuild minimal axis-aligned polygons around clusters, actively exclude sardines by\nkeeping polygons tight. Try diverse constructions: single cluster boxes, multi-cluster combos.\nUse KD-tree for fast fish counting. Run multiple diverse candidates per eval, probe then evaluate."
---

# Mackerel-Focused Clustering Strategy

## Phase 1: Spatial Analysis
- Parse all mackerel and sardine coordinates from input
- Build KD-tree or grid for efficient spatial queries
- Find mackerel clusters: groups of mackerels within distance 5000 of each other

## Phase 2: Cluster Enclosure
For each identified mackerel cluster:
- Compute minimal axis-aligned bounding box
- Check sardine count inside (should be low if cluster is isolated)
- Compute score = M - S + 1

## Phase 3: Multi-Cluster Combinations
- Try combining adjacent clusters into larger polygons
- Consider: combined score of separate polygons vs single large polygon
- Generally prefer separate polygons if they don't overlap

## Phase 4: Diverse Generation
- Generate multiple candidate approaches:
  * Approach A: Single large polygon covering many mackerels
  * Approach B: Multiple small polygons around individual clusters  
  * Approach C: Hybrid (large + small)
- Use KD-tree to quickly estimate sardine counts for ranking

## Phase 5: Validation and Output
- Validate each candidate: 4-1000 vertices, valid coordinates, no self-intersection
- Output the best candidate (highest M - S + 1)
- Always output at least one valid polygon

## C++ Implementation Notes
- Use input parsing to read fish positions
- Implement efficient spatial indexing (KD-tree or grid)
- Generate multiple diverse polygons per evaluation
- Use probe if available for quick ranking
- Ensure <2.0s execution time

Mackerels are the friend to capture, sardines are the penalty to avoid.
Build TIGHT polygons around mackerel clusters, not loose ones.
