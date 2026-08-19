---
name: discovery-optimization
description: "Optimize C++ for fish-capture polygon maximization using a REGION-FIRST strategy. Focus on identifying high mackerel / low sardine density regions, constructing tight polygons around them, using L-shaped variants, and employing probe-based candidate ranking before full evaluation."
---

# Polygon Optimization for Fish Capture

## Problem Recap
- Maximize: mackerels_inside - sardines_inside + 1
- Polygon: axis-aligned (edges parallel to x or y), max 1000 vertices, perimeter ≤ 400,000
- Fish positions: N=5000 mackerels, N=5000 sardines at distinct integer coordinates
- Time limit: ~2.0s per evaluation for internal search

## Core Strategy: Active Search with Spatial Indexing

### Step 1: Fast Fish Counting
- Use a grid or KD-tree for O(1) or O(log N) fish count queries in any rectangle
- Pre-process fish into spatial index at startup
- This enables O(1) scoring of candidate polygons

### Step 2: Polygon Construction Pipeline
Start with a baseline (bounding box of mackerels), then try:
- **Rectangular search**: Try many bounding boxes, keep best
- **L-shaped polygons**: Combine two rectangles to capture corner clusters
- **Stepped polygons**: Create staircase patterns around dense mackerel regions
- **Exclude sardines**: Gently indent polygon edges near sardine clusters

### Step 3: Iterative Refinement
- From best polygon, try edge perturbations (±1 to ±10 units)
- Keep modifications that increase score
- Use local search (hill climbing) with multiple random restarts

### Step 4: Time Budget Management
- Allocate time: 0.1s setup, 0.5s baseline construction, 1.0s refinement, 0.4s final polish
- Use early termination if score stops improving for 0.1s
- Always stop with VALID polygon even if score is suboptimal

## Key C++ Patterns

```cpp
// Grid-based counting (fast for axis-aligned queries)
int count_in_grid(int minX, int maxX, int minY, int maxY) {
    int sum = 0;
    for (int x = minX; x <= maxX; x += CELL_SIZE) {
        for (int y = minY; y <= maxY; y += CELL_SIZE) {
            // count all fish in this cell
        }
    }
    return sum;
}

// L-shape construction: capture top-right corner
vector<Point> make_L_shape(int mx_left, int mx_top, int sx_bottom, int sx_right) {
    // Returns 6 vertices: bounding box minus bottom-left or top-right corner
}

// Local refinement: try edge perturbations
vector<Point> refine_polygon(const vector<Point>& poly, int max_delta) {
    // Try moving each edge by ±delta, keep best
}
```

## Common Pitfalls
- Don't search indefinitely - use timeout!
- Don't forget to output a VALID polygon (non-self-intersecting, axis-aligned)
- Don't hardcode a single polygon - search actively
- Don't ignore sardines - subtracting them hurts score significantly
- Watch perimeter constraint (400,000 max)

## Evaluation Feedback Loop
- If validity=0: fix the polygon construction bug
- If score < expected: try different polygon shapes
- If timeout: reduce search iterations or use faster counting
- If score > baseline: exploit by refining further
