---
name: discovery-optimization
description: "KD-tree powered rectangle search with union-of-rectangles support. Use KD-tree for fast O(log N) rectangle queries, generate candidate rectangles, try unions of 2-4 rectangles, refine edges with \u00b15..50 shifts, validate constraints strictly."
---

# KD-Tree Powered Rectangle Optimization

## Core Strategy

The problem requires finding an axis-aligned polygon that maximizes (mackerels - sardines + 1). The seed program includes a KD-tree for efficient spatial queries - this is your primary tool.

## Method: Rectangle-Based Search

### Phase 1: Rectangle Generation
1. Sample random corner pairs (x1,y1) and (x2,y2) where x1≤x2, y1≤y2
2. Ensure resulting rectangle is valid: perimeter = 2*(width+height) ≤ 400,000
3. Query the rectangle using KD-tree for fish counts
4. Score = mackerels - sardines
5. Keep best rectangle found

### Phase 2: Union of Rectangles (Advanced)
1. Generate 2-4 rectangles with good individual scores
2. Merge them carefully:
   - If rectangles overlap, use inclusion-exclusion to count fish
   - Ensure union forms a valid simple polygon
3. Score the merged region
4. This can capture fish in disjoint clusters more effectively than single rectangles

### Phase 3: Edge Refinement
1. For each edge of best polygon, try shifts: ±5, ±10, ±20, ±50 units
2. Use KD-tree to query new rectangle
3. Keep shifts that improve score
4. Repeat 2-3 rounds

### Phase 4: Random Polygon Generation
1. Generate non-rectangular polygons (L-shapes, U-shapes, etc.)
2. Build from seed points
3. Validate constraints
4. Score using KD-tree

### Phase 5: Multiple Restarts
1. Run 20-30 restarts with different random seeds
2. Each restart: generate candidate polygons, refine, track best
3. Output single best polygon

## Implementation Notes

- KD-tree query complexity: O(k + log N) where k = fish in rectangle
- Rectangle generation: sample corners uniformly or bias toward high-density regions
- Edge refinement: only shift if it doesn't violate constraints
- Always validate: perimeter, vertices, bounds, self-intersection
- Total time per eval: < 2.0s

## Success Criteria
- Average score > 5000 (target from task description)
- Valid output for all 150 test cases
- No self-intersecting polygons
- Perimeter constraint respected
