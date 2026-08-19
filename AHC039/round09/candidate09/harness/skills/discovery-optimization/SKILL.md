---
name: discovery-optimization
description: "Cluster-based rectangular construction. Detect mackerel clusters via proximity, build axis-aligned rectangles around each, strategically connect adjacent high-value rectangles, multiple restarts."
---

# Cluster-Based Rectangular Construction Strategy

## Phase 1: Cluster Detection
- Read all mackerel coordinates from input
- Use proximity-based clustering (radius ~8000) to group nearby mackerels
- Each cluster represents a potential polygon region

## Phase 2: Rectangle Construction
For each cluster:
- Compute bounding box: (min_x, min_y) to (max_x, max_y)
- Create axis-aligned rectangle with 4 vertices
- Count mackerels and sardines inside rectangle
- Score = mackerels - sardines + 1
- Keep only rectangles with positive score

## Phase 3: Strategic Connections
- Sort rectangles by score descending
- For each pair of adjacent rectangles (share edge or close):
  - Compute combined polygon (union of rectangles)
  - Score the combined polygon
  - If combined score > individual scores, keep connection
- Maximum 5 rectangles per final polygon

## Phase 4: Multiple Restarts
- Run 20 restarts with different random seeds
- Each restart:
  * Slightly perturb cluster centers (add random offset)
  * Re-run clustering and rectangle construction
  * Try different connection strategies
- Track best polygon across all restarts

## C++ Implementation Notes
- Use O(N log N) clustering via sort and sweep
- Rectangle scoring via point-in-rectangle tests
- Combined polygon scoring via vertex iteration
- Total time per evaluation: < 2.0s
- Include simple self-intersection check for polygon validity
