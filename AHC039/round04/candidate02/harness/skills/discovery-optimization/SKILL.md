---
name: discovery-optimization
description: "Polygon heuristic optimization: Build axis-aligned polygons to maximize mackerel catch while avoiding sardines.\nUse region analysis and targeted shape mutations."
---

# Polygon Heuristic Optimization Method

## Objective
Maximize: score = max(0, mackerels_inside - sardines_inside + 1)

## Constraints
- Vertices: 4 to 1000
- Perimeter: ≤ 400,000
- Coordinates: integers in [0, 100000]
- Edges: axis-aligned (horizontal or vertical only)
- Simple polygon (no self-intersection)

## Search Strategy

### Phase 1: Analysis (first 10-15% of time)
1. Load current best polygon
2. Compute perimeter check
3. Identify "hot zones":
   - Mackerel density regions (need polygon extension)
   - Sardine clusters (need polygon exclusion/shrinkage)
4. Calculate current score estimate

### Phase 2: Mutation Operators

**Type A: Exploit Mutations** (capture more mackerels)
- Find mackerel points near current polygon boundary
- Extend boundary outward by 1-2 units to include them
- Ensure no new sardines are added

**Type B: Avoid Mutations** (reduce sardines)
- Find sardine points near current polygon boundary
- Retract boundary inward, or create indentations
- Cut off corners that enclose sardines

**Type C: Shape Optimizations**
- Round out corners to capture diagonal clusters
- Split large compartments to avoid sardine pockets
- Create "fingers" into mackerel-rich corridors

### Phase 3: Validation Before Evaluation
For each proposed variant:
1. Check perimeter: sum of edge lengths ≤ 400,000
2. Check vertex count: ≤ 1,000
3. Check axis-alignment: all edges horizontal or vertical
4. Check simplicity: no edge overlaps (use winding number or ray casting mentally)
5. Check coordinate range: all points in [0, 100000]²
6. Check distinct vertices

Only evaluate VALID variants. Discard invalid proposals silently.

### Phase 4: Iterative Loop
Loop until time limit (save 0.1s margin):
1. Analyze current best polygon
2. Generate 3-5 variants using the above operators
3. Validate each variant
4. Evaluate top 1-2 valid variants
5. Keep best-scoring variant
6. Check if score improved significantly
7. If no improvement for 5+ iterations, try different mutation types

### Emergency Handoffs
If score is low:
- Try simpler shapes (rectangle, L-shape) first
- Consider completely different layout if stuck

## Time Budget
Target 1.85-1.9 seconds per evaluation. Always measure and adjust.
