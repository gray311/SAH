---
name: discovery-optimization
description: "Optimize C++ polygon-constructing code for fish-capture maximization. Use scan_rectangles() for rapid\nmackerel cluster detection, then build L-shapes/stepped polygons that exclude sardine hotspots.\nImplement corner-focused expansion and local edge refinement with multiple random restarts."
---

# Fish Capture Polygon Optimization

## Core Strategy

This problem rewards polygons that capture mackerels while avoiding sardines. Key insights:
- Fish positions are fixed; find the best enclosing shape
- Mackerels likely cluster in certain regions; sardines in others
- Axis-aligned polygons can cleverly "exclude" sardine clusters by indenting edges

## Search Pipeline

### Phase 1: Rapid Rectangle Scanning (scan_rectangles)
- Sample ~50-100 random rectangles covering the coordinate space
- Score each quickly (use grid/KD-tree for O(1) counts)
- Keep top 5-10 rectangles by score
- Time budget: 0.3s

### Phase 2: L-Shape and Stepped Polygon Construction
- For each promising rectangle, try excluding sardine clusters by:
  * Cutting out the bottom-left/top-right corner region where sardines cluster
  * Creating stepped patterns that follow mackerel boundaries
- Generate 3-5 variants per rectangle
- Score quickly (probe if available)
- Time budget: 0.5s

### Phase 3: Corner-Focused Expansion
- Fish often cluster at boundaries/corners of the feasible region
- Expand polygon toward coordinate extremes (0 or 100000) if that adds mackerels
- Use multi-objective: maximize mackerels while minimizing sardine penalty
- Time budget: 0.3s

### Phase 4: Local Edge Refinement
- For best polygon, try perturbing each edge by ±1 to ±10 units
- Accept only moves that increase score
- Run hill climbing with 5-10 random restarts from different seeds
- Time budget: 1.0s

### Phase 5: Final Validation
- Ensure polygon is non-self-intersecting, axis-aligned, within perimeter limit
- Output the best valid polygon found

## C++ Implementation Patterns

```cpp
// Phase 1: scan_rectangles
struct Rect { int x1, y1, x2, y2; };
vector<Rect> sample_rectangles(int count) {
    // Random rectangles covering [0, 100000]x[0, 100000]
}
int score_rect(const Rect& r) {
    // Count mackerels and sardines inside rectangle using KD-tree or grid
}

// Phase 2: L-shape construction
vector<Point> make_L_shape(const vector<Point>& rect, int cut_type) {
    // Cut out a corner region to exclude sardines
}

// Phase 3: Corner expansion
vector<Point> expand_toward_corner(const vector<Point>& poly, int corner) {
    // Move edges toward (0,0), (0,100000), (100000,0), or (100000,100000)
}

// Phase 4: Local refinement
vector<Point> refine_polygon(const vector<Point>& poly, int max_delta, int restarts) {
    // Try edge perturbations, keep best
}
```

## Avoid These Pitfalls

- Don't just use one rectangle - search many candidates
- Don't ignore sardines - they significantly hurt the score
- Don't exceed perimeter limit (400,000) or vertex limit (1000)
- Don't forget to output a VALID polygon (non-self-intersecting)
- Don't waste time - use timeouts and stop early if no improvement
- Use probe_solution for quick rectangle testing when available

## Time Budget Allocation

Total: 2.0s per evaluation
- Setup: 0.1s
- Rectangle scanning: 0.3s
- L-shape/stepped construction: 0.5s
- Corner expansion: 0.3s
- Local refinement: 1.0s
- Validation/output: 0.1s
