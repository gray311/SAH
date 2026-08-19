---
name: cluster-guided-search
description: Method playbook - Use cluster analysis to guide polygon construction. Build polygons around dense mackerel clusters while excluding nearby sardines. Start with cluster centroids, expand to bounding boxes, then refine with stepped polygons to avoid sardines.
---

# Cluster-Guided Search Strategy

## Step 1: Cluster Analysis (MANDATORY)
- Call analyze_mackerel_clusters at the start
- Identify top 3 clusters by density
- For each cluster, compute:
  * Centroid (mean x, y)
  * Bounding box
  * Distance to nearest sardine

## Step 2: Polygon Construction Pipeline

### Option A: Single Cluster Bounding Box
- Create rectangle around cluster centroid
- Extend by 2000 units in all directions
- Calculate score using quick_score_rect

### Option B: Stepped Polygon (Recommended)
- Start with bounding box
- For each edge, check if sardines are nearby
- If sardine < 500 units from edge, indent the edge inward
- Create staircase pattern: move edge inward, then parallel offset
- This excludes sardines while keeping mackerels

### Option C: L-Shaped Polygon
- If sardines form a line or cluster near one corner
- Use L-shape to step around the sardine cluster
- Vertices: (min_x, min_y) -> (max_x, min_y) -> (max_x, sardine_y) -> 
             (sardine_x, sardine_y) -> (sardine_x, max_y) -> (min_x, max_y) -> (min_x, min_y)

## Step 3: Multi-Cluster Combination
- If top 2 clusters are close (< 5000 units apart)
- Try combining with a connecting rectangle
- Score the combined shape

## Step 4: Local Refinement
- From best polygon, try edge perturbations
- For each edge, try moving by ±1, ±2, ..., ±10 units
- Keep only improvements
- Limit to 100 refinement attempts

## Step 5: Validation
- Ensure polygon is non-self-intersecting
- Check perimeter ≤ 400,000
- Ensure vertices are integers
- Output in correct format
