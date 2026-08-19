---
name: discovery-optimization
description: "Find optimal unions of disjoint axis-aligned rectangles for fish capture.\nEach rectangle contributes (mackerels_inside - sardines_inside) to score.\nUse clustering to identify mackerel-dense, sardine-poor regions.\nBuild and evaluate multiple rectangle candidates, combine best ones.\nRespect perimeter \u2264400,000 and vertex \u22641000 constraints."
---

# Optimal Rectangle Union Strategy for Fish Capture

## Problem Understanding
- Maximize: sum over all rectangles of (mackerels - sardines + 1)
- Each rectangle is axis-aligned, vertices at integers 0-100000
- Rectangles in the union should be disjoint (or touch at edges)
- Total perimeter ≤ 400,000, vertices ≤ 1000

## Algorithm: Rectangle Union Search

### Phase 1: Cluster Analysis
1. Read all fish positions
2. Build a grid (cell size ~100-200) of fish density
3. Identify "hotspots": regions with many mackerels, few sardines
4. For each hotspot, compute a maximal rectangle

### Phase 2: Rectangle Construction
For each identified hotspot:
- Find the bounding box of mackerels in that region
- Expand outwards while avoiding sardines (stop when hitting sardine)
- Record rectangle: (x1, y1, x2, y2)

### Phase 3: Combination Optimization
- Start with all candidate rectangles
- For each pair, check if they overlap (if so, merge or remove one)
- Score each valid combination
- Use hill climbing: try adding new rectangles, removing weak ones
- Stop when no improvement in 5-10 iterations

### Phase 4: Validity Check
- Ensure total perimeter ≤ 400,000
- Ensure vertices ≤ 1000
- Output rectangles as a single valid polygon (concatenate vertex lists)

## Key Implementation Patterns

```cpp
struct Rectangle { int x1, y1, x2, y2; };

// Count fish in rectangle (using pre-built spatial index)
int count_in_rect(Rectangle r, const std::vector<Fish>& fish, const Grid& grid) {
    int mackerels = 0, sardines = 0;
    for (int x = r.x1; x <= r.x2; x += CELL_SIZE) {
        for (int y = r.y1; y <= r.y2; y += CELL_SIZE) {
            mackerels += grid.count_mackerels(x, y);
            sardines += grid.count_sardines(x, y);
        }
    }
    return mackerels - sardines + 1;
}

// Find maximal rectangle for a seed point
Rectangle make_maximal_rect(int sx, int sy, const std::vector<Fish>& fish, const Grid& grid) {
    Rectangle r = {{sx, sy, sx, sy}};
    // Expand in all 4 directions while no sardines
    while (can_expand(r.x1, r.y1) && !has_sardine(r.x1-1, r.y1)) { r.x1--; }
    while (can_expand(r.x2, r.y2) && !has_sardine(r.x2+1, r.y2)) { r.x2++; }
    // ... same for y
    return r;
}
```

## Time Budget Allocation
- Grid setup: 0.05s
- Initial cluster detection: 0.1s
- Rectangle generation: 0.2s
- Combination optimization loop: 1.5s (hill climbing)
- Final validation: 0.15s
- Total: ~2.0s (use full budget)
