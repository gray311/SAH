---
name: discovery-optimization
description: "Bounding-box refinement for mackerel clusters. Detect dense clusters, expand each box to include fish with positive net gain, merge overlapping boxes, build polygon via x-order traversal, refine with corner shifts."
---

# Bounding-Box Refinement Strategy

## Phase 1: Cluster Detection
- Read all mackerel positions from input
- Use spatial hashing (bucket positions into 500x500 grids)
- Identify clusters: cells with >= 3 mackerels within same bucket or adjacent buckets
- For each cluster, compute tight bounding box

## Phase 2: Directional Box Expansion
For each cluster box, expand in all 4 directions:
- Start from current box edge
- Add one unit width in a direction if:
  * The new strip (all cells in that direction from edge) has more mackerels than sardines
  * Net gain = (new mackerels in strip) - (new sardines in strip) > 0
- Expand until net gain <= 0 or boundary reached
- Track which fish are newly included

## Phase 3: Polygon Merging
- Collect all expanded boxes
- If any two boxes overlap or are within 2000 units, merge them
- Compute the minimal axis-aligned union polygon
- For non-overlapping boxes, create separate polygons (use largest one)

## Phase 4: Corner Refinement
For the resulting polygon:
- For each corner (up to 1000):
  * Try shifting by ±5, ±10, ±20 units in both directions
  * Estimate new score using box contributions
  * Keep shifts that improve the score
- Repeat 2-3 rounds of refinement

## Phase 5: Multiple Restarts
- Run 10-15 independent restarts:
  * Each restart: randomly select 1-3 mackerel clusters
  * Build and expand boxes for selected clusters
  * Merge and refine
- Output the best polygon from all restarts

## Implementation Notes
- Use O(N) spatial hashing for cluster detection
- Pre-compute mackerel/sardine counts in grid cells
- Box expansion runs in O(width × height) per direction
- Corner refinement uses O(vertices × 12) evaluations
- Total per restart: < 0.5 seconds
- Ensure all coordinates are integers and within bounds
