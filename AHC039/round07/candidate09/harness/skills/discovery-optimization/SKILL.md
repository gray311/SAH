---
name: discovery-optimization
description: "Optimize C++ polygon-constructing code for NP-hard fish-capture maximization using CLUSTER-BASED\nstructural search. Build polygons that create bite-outs around sardine clusters and form multi-rectangular\nshapes around mackerel clusters. Use spatial analysis to guide construction, not incremental refinement."
---

# Cluster-Based Polygon Optimization for Fish Capture

## Problem Recap
- Maximize: mackerels_inside - sardines_inside + 1
- Polygon: axis-aligned (edges parallel to x or y), max 1000 vertices, perimeter ≤ 400,000
- N = 5000 mackerels, N = 5000 sardines at distinct integer coordinates
- Time limit: ~2.0s per evaluation for internal search

## Core Strategy: Cluster Analysis + Structural Construction

### Step 1: Build Spatial Index (0.2s)
- Read all fish positions
- Build grid or KD-tree for O(1) fish counting in any rectangle
- This enables fast scoring of candidate polygons

### Step 2: Identify Clusters (0.3s)
- **Mackerel clusters**: Find regions with high mackerel density
- **Sardine clusters**: Find regions with high sardine density (these are "costs")
- Use distance-based clustering: if fish within 500-1000 units, they form a cluster

### Step 3: Construct Candidate Polygons (0.8s)
Build 3-5 structurally different polygons:

**Base Polygon**: Bounding box of all mackerels
- Simple rectangle covering all mackerel x-range and y-range
- Count fish, record score

**Bite-Out Polygons**: For each sardine cluster:
- Start with base polygon
- Identify the sardine cluster's bounding box
- Create an indentation (bite-out) in one edge to exclude sardines
- Cost: adds 2-4 vertices, may slightly reduce mackerel capture
- Net effect: if sardines > mackerels in that region, score improves

**Multi-Rectangular Polygons**: For separated mackerel clusters:
- If mackerels form 2+ distinct clusters, create separate rectangles
- Connect them with narrow corridors (if needed for validity)
- Can capture high-density regions while avoiding sparse (sardine-rich) areas

**Stepped Polygons**: Follow density contours:
- Create staircase-like edges around dense mackerel regions
- Each "step" adds 2 vertices
- Better captures irregular density distributions than simple rectangles

### Step 4: Score and Select (0.4s)
- Count fish in each candidate polygon
- Score = mackerels - sardines + 1
- Keep the best-scoring valid polygon
- Output its vertices

## Implementation Patterns

```cpp
// Grid-based cluster detection
void detect_clusters(const vector<Fish>& fish, int grid_size, 
                     vector<vector<int>>& cluster_ids) {
    // Group fish by grid cell, merge adjacent cells with same dominant species
}

// Bite-out construction
vector<Point> make_bite_out_polygon(const vector<Point>& base, 
                                    const vector<Point>& bite_rect,
                                    int edge_side) {
    // Insert vertices to create indentation on the specified edge
    // Example: on top edge, create a downward-pointing rectangle
}

// Stepped polygon from density contours
vector<Point> make_stepped_polygon(const vector<vector<int>>& density_grid,
                                   int max_steps_per_side) {
    // Traverse density grid, create staircase following high-density regions
}

// Multi-rectangular construction
vector<Point> make_multi_rect_polygon(
    const vector<Cluster>& mackerel_clusters,
    const vector<Point>& connect_points) {
    // Build separate rectangles for each cluster, connect with corridors
}
```

## Evaluation Feedback

- If score < expected for bite-out: the sardine cluster may be too sparse
- If multi-rect doesn't help: mackerels may be in one large cluster
- If stepped fails: simple bounding box may already be optimal for that distribution
- Always ensure polygon validity: no self-intersections, axis-aligned edges
