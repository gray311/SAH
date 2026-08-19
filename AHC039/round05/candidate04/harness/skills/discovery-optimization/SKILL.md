---
name: discovery-optimization
description: "Iteratively optimize a geometric algorithm to maximize mackerel capture minus sardine catch in rectilinear polygons. Focus on constructive geometric strategies with bounding boxes and orthogonal polygon design."
---

# Rectilinear Polygon Optimization for Mackerel-Sardine Capture
## Objective Maximize: (count of mackerels inside) - (count of sardines inside) + 1
## Constraints - Orthogonal polygon (edges parallel to x or y axes) - Max 1000 vertices, perimeter <= 400,000 - Integer coordinates 0-100,000 - No self-intersections
## Strategy Framework
### Phase 1: Data Analysis 1. Call analyze_geometry() ONCE early to understand: - Mackerel bounding box and cluster distribution - Sardine locations relative to mackerels - Potential high-density regions
### Phase 2: Polygon Construction Strategies Try these approaches sequentially, varying parameters:
A. Single Bounding Box - Find the bounding box covering most mackerels - Compute: count_mackerels - count_sardines - Try centers, expanded boxes, shrunk boxes
B. Multiple Rectangles - Partition mackerels into clusters - Build separate rectangles for each cluster - Combine into one orthogonal polygon (chain rectangles)
C. Bounding Box of Mackerel Subset - Select top-k densest mackerel regions - Take union of their bounding boxes - Create orthogonal polygon from union
D. Constraint-Aware Expansion - Start with tight mackerel cluster box - Expand outward until hitting sardine boundaries - Clip sardines from interior
E. Sweep-Line Grid - Divide space into grid cells - Fill cells with >threshold mackerels - Merge adjacent filled cells into orthogonal polygon
### Phase 3: Optimization Loop For each strategy: 1. Vary seed mackerels (subset selection) 2. Vary expansion/contraction parameters 3. Vary rectangle merging rules 4. Probe multiple variants, select best 5. Full evaluate only on top 1-2 candidates
### Phase 4: Validation Before submit: - Check perimeter <= 400,000 - Check vertices <= 1000 - Ensure no self-intersections - Verify all mackerel/sardine counts
## Key Insights - Simple rectangles often outperform complex polygons for this task - Focus on mackerel density, not just raw count - Avoid rectangles with many sardines inside - A single tight box around a cluster may beat a loose large box - The KD-tree in the seed is useful for fast counting - preserve and enhance it - Time budget ~1.9s per test case - avoid O(N^2) internal searches
## Execution Plan 1. Call analyze_geometry() -> understand data 2. Edit solution with Strategy A, probe it 3. If poor, try Strategy B with different clustering 4. Probe variants to rank, evaluate top 1-2 5. Iterate with refinements until eval budget exhausted 6. Call finish() with summary
