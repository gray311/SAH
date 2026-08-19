---
name: point-clustering-guide
description: Cluster mackerels by proximity, build tight BBoxes per cluster, merge with MST corridors, refine edges
---

# Point-Level Clustering Strategy for Polygon Construction

## Core Idea

Instead of coarse grid abstraction, cluster mackerels by actual spatial proximity at the coordinate level, then build tight axis-aligned bounding boxes that can be precisely shaped to exclude sardines.

## Step-by-Step Method

### Step 1: Point-Level Clustering

- Read all mackerel coordinates from input (N=5000 points)
- Use distance-based clustering with threshold ~10000 units
- For each unclustered mackerel, find nearest neighbor; if distance < threshold, merge clusters
- Result: groups of spatially proximate mackerels

### Step 2: Tight Bounding Box Computation

- For each cluster, compute:
  * min_x = minimum x coordinate in cluster
  * max_x = maximum x coordinate in cluster  
  * min_y = minimum y coordinate in cluster
  * max_y = maximum y coordinate in cluster
- This gives a tight axis-aligned rectangle around each cluster

### Step 3: Sardine Boundary Check

- For each cluster's bounding box, check all sardines
- If any sardine has x in [min_x-100, max_x+100] and y in [min_y, max_y] (or vice versa),
  the sardine is near/inside the boundary
- Mark boundaries that need expansion

### Step 4: Boundary Expansion

- For each marked boundary, expand outward until no sardines are near the edge
- Use binary search if needed for precision
- Ensure expanded coordinates stay in [0, 100000]

### Step 5: MST-Based Merging

- Compute pairwise min-distances between all rectangle pairs
- Build MST using Kruskal's or Prim's algorithm
- For each MST edge, create a corridor rectangle connecting the two parent rectangles
- Corridor should be the minimum rectangle that bridges the two parent rectangles

### Step 6: Local Edge Refinement

- For each edge of the final polygon:
  * Try expanding by +50, +100, +200 units
  * Try shrinking by -50, -100, -200 units (if doesn't exclude mackerels)
  * Use rectangle query for fast scoring
  * Accept if score improves
- Repeat 5-10 iterations

### Step 7: Multiple Strategy Ensemble

Try these approaches and pick best:
- Single rectangle around all mackerels
- Per-cluster rectangles with MST connections
- Convex hull approximation (project to axis-aligned)
- Greedy expansion from densest cluster

## Key Success Factors

- Point-level precision allows tight exclusion of boundary sardines
- MST merging creates connected polygon while minimizing corridor overhead
- Local refinement fine-tunes edge positions
- Ensemble approach hedges against strategy-specific weaknesses
