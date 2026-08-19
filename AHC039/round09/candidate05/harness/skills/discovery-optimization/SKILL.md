---
name: discovery-optimization
description: "Local cluster isolation. Find clean mackerel clusters (no sardines within 3 units), build tight bounding box polygons, refine with \u00b11..3 edge expansions, 20 restarts with diverse cluster selections."
---

# Local Cluster Isolation Strategy

## Core Principle
Instead of trying to connect distant mackerels through corridors, focus on finding tight clusters of mackerels that can be enclosed by a small polygon without any sardines.

## Step 1: Clean Mackerel Identification
- For each mackerel at position (x, y), check all points (x', y') where |x-x'| ≤ 3 AND |y-y'| ≤ 3
- If no sardine exists in this 7x7 region (centered on mackerel), mark as "clean"
- This 3-unit radius is small enough that random distributions often have clean pockets

## Step 2: Cluster Formation
- Group clean mackerels that are close to each other (distance ≤ 10 units)
- Use Union-Find or BFS to identify connected components
- Each component becomes a candidate cluster

## Step 3: Polygon Construction
- For each cluster, compute tight axis-aligned bounding box
- Vertices: (min_x, min_y) → (max_x, min_y) → (max_x, max_y) → (min_x, max_y)
- This forms a 4-vertex rectangle (valid if max_x > min_x and max_y > min_y)
- Verify all cluster mackerels are inside or on boundary
- Verify NO sardines inside or on boundary (critical!)

## Step 4: Safe Expansion
- For each edge of the polygon, try expanding outward by ±1, ±2, ±3 units
- After each expansion, re-verify:
  * Still contains all cluster mackerels
  * Does NOT contain any new mackerels (unless desired)
  * Does NOT contain any sardines
- Keep expansions that maintain safety (no sardines)
- Repeat for up to 10 iterations per edge

## Step 5: Cluster Merging (Optional)
- Try combining two adjacent clusters into one polygon
- New polygon = bounding box of union of both clusters
- Only merge if expanded box still excludes all sardines
- This can capture more mackerels with minimal penalty risk

## Step 6: Multiple Restart Strategies
- **Random Subset**: Pick random clean mackerels, form cluster, build polygon
- **Largest First**: Sort clusters by mackerel count, pick largest
- **Density**: Pick mackerels with most nearby clean mackerels
- **Grid Search**: Divide domain into fine grid, pick mackerel with highest local density

## Step 7: Output Selection
- Evaluate each candidate polygon's score (mackerels - sardines + 1)
- Output the single polygon with highest score
- If no valid polygon found, output minimal 4-vertex polygon with at least 1 mackerel

## Implementation Notes
- Use exact coordinate comparisons (no floating point)
- Point-in-rectangle check: min_x ≤ x ≤ max_x AND min_y ≤ y ≤ max_y
- Sardine exclusion is CRITICAL: any sardine inside = score penalty
- Time budget: < 2.0s per evaluation, aim for 15-20 candidate polygons
