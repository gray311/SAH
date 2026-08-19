---
name: discovery-optimization
description: "Cluster-based rectangle construction. Parse fish coordinates, group mackerels by proximity, build tight axis-aligned rectangles around clusters, refine boundaries, try multi-rectangle unions, 10 restarts."
---

# Cluster-Based Rectangle Construction for Polygon Optimization

## Core Idea

Directly use fish coordinates to build tight axis-aligned rectangles around mackerel clusters, then refine boundaries.

## Step-by-Step Method

### Step 1: Parse and Store Coordinates

- Read all mackerel and sardine coordinates from input
- Store as vectors of Point structs
- N = 5000 for both types

### Step 2: Cluster Mackerels by Proximity

- Use a simple clustering: for each unclustered mackerel, start a new cluster
- Add nearby mackerels (distance <= 500) to the cluster
- Merge clusters if they're within 300 units
- Identify clusters with 5+ mackerels as "significant"

### Step 3: Build Tight Bounding Rectangles

For each significant cluster:
- Compute min_x, max_x, min_y, max_y across all mackerels in cluster
- Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- Count mackerels inside (should be all cluster members, plus any nearby)
- Count sardines inside the rectangle

### Step 4: Rectangle Refinement

For each rectangle candidate:
- Try expanding each side by ±1, ±2, ±3 units
  - If expansion captures more mackerels and doesn't add too many sardines, accept
- Try shrinking each side by ±1, ±2 units
  - If shrinking excludes sardines while keeping all mackerels, accept
- Keep the refinement that maximizes (mackerels - sardines)

### Step 5: Multi-Rectangle Strategy

- If best single rectangle has score < 1000, try combinations:
  - Pick 2-3 non-overlapping (or minimally overlapping) significant clusters
  - Build their rectangles
  - Compute union as polygon (up to 12 vertices for 3 rectangles)
  - Score the union

### Step 6: Multiple Restarts

- Run 10 restarts with different random seeds
- Each restart: use different random perturbations in clustering
- Track best polygon across all restarts

### Step 7: Validation and Output

- Ensure polygon has 4-1000 vertices
- Ensure perimeter <= 400,000
- Ensure all coordinates in [0, 100000]
- Check for self-intersection
- Output in format: m then m lines of "x y"

## C++ Implementation Notes

- Use O(N) clustering (simple distance-based, not KD-tree)
- Rectangle queries are O(1) once coordinates are stored
- Total time per evaluation: < 2.0s
- Use std::sort and binary search for efficient coordinate queries
