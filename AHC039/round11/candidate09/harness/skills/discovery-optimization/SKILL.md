---
name: discovery-optimization
description: "KD-tree based vertex refinement. Use KD-tree for fast accurate rectangle scoring. Start with bounding box, then iteratively refine each vertex with small integer perturbations (\u00b11..5). Add/remove corners to create complex shapes. Build multi-lobed polygons around separate mackerel clusters. Validate polygon simplicity and constraints."
---

# KD-Tree Based Polygon Optimization Strategy

## Overview
This strategy uses the seed's KD-tree data structure for fast, accurate fish counting in any axis-aligned rectangle. Unlike grid-based approximations, KD-tree provides exact counts in O(log N) time, enabling fine-grained optimization.

## Phase 1: Initial Polygon Construction

### Option A: Global Bounding Box
- Find min_x, max_x, min_y, max_y among all fish
- Create a 4-vertex rectangle [min_x, max_x, min_y, max_y]
- Score this initial polygon using KD-tree

### Option B: Mackerel-Cluster Based
- Query KD-tree for regions with high mackerel density
- For top 3-5 clusters, create rectangular bounding boxes
- Combine into a single polygon (union of rectangles)

## Phase 2: Vertex Refinement Loop

For each vertex (up to 1000) of the current polygon:

1. **Horizontal edges** (vertex i to i+1):
   - Current vertex: (x, y)
   - Try new y-coordinates: y-5, y-4, ..., y-1, y+1, ..., y+5
   - For each candidate, create modified polygon and score via KD-tree
   - Keep best perturbation

2. **Vertical edges** (vertex i to i+1):
   - Current vertex: (x, y)
   - Try new x-coordinates: x-5, x-4, ..., x-1, x+1, ..., x+5
   - Score each variant using KD-tree
   - Keep best perturbation

3. **Corner vertices** (where edge direction changes):
   - Try expanding: shift both x and y outward (+1, +2, +3, +4, +5)
   - Try contracting: shift both x and y inward (-1, -2, -3, -4, -5)
   - Score each variant using KD-tree
   - Keep best perturbation

**Termination**: Stop when no perturbation improves score after one full pass through all vertices.

## Phase 3: Corner Addition/Removal

### Adding Corners (to capture more fish)
- For each long edge, try inserting a corner point:
  - Pick midpoint of edge
  - Try extending perpendicular by 1-5 units
  - Score the new polygon (now 5+ vertices)
  - Keep if score improves

### Removing Corners (to reduce perimeter cost)
- Identify collinear consecutive vertices
- Merge them into one vertex
- Score the simplified polygon
- Keep if score improves (usually same score, but fewer vertices)

**Note**: Only add corners if the extra perimeter cost is offset by fish captured.

## Phase 4: Multi-Lobe Construction

1. Query KD-tree to find separate high-density mackerel regions
   - For each (x, y) region of size 1000x1000, count mackerels/sardines
   - Identify 3-5 top regions

2. Create a rectangular "lobe" for each region:
   - Find bounding box of mackerels in region
   - Expand slightly to include boundary fish
   - Score the lobe

3. Combine lobes into a single polygon:
   - Use a union algorithm (merge overlapping/adjacent rectangles)
   - Result may have 4-500 vertices
   - Score the combined polygon

4. Apply Phase 2 refinement to the combined polygon

## Phase 5: Constraint Validation

Before output, verify:
- Vertex count: 4 <= m <= 1000 ✓
- Perimeter: <= 400,000 ✓
- Coordinates: 0 <= x, y <= 100,000 ✓
- No self-intersection ✓
- All vertices distinct ✓

If any constraint violated, either:
- Remove vertices (merge collinear ones)
- Scale down coordinates proportionally (if out of bounds)
- Split into multiple valid polygons (pick best one)

## Phase 6: Multiple Restarts

Run the above strategy 10-15 times with different:
- Initial seed (bounding box vs cluster-based)
- Vertex refinement starting points
- Corner addition patterns

Output the best polygon across all restarts.

## Complexity Analysis
- KD-tree build: O(N log N) once
- Each KD-tree query: O(log N)
- Vertex refinement per vertex: ~10 queries × 5 perturbations = 50 queries
- Total queries per eval: ~1000 vertices × 50 queries / 100 iterations = 500-1000 queries
- With N=5000, log N ≈ 13, so 1000 × 13 ≈ 13,000 operations (fast enough for 2s limit)
