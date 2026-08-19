---
name: discovery-optimization
description: "Geometric optimization harness for axis-aligned polygon construction. Load this skill to implement\nspatial analysis-driven polygon design with multi-strategy exploration and probe-based filtering."
---

# Geometric Polygon Optimization for Fish Capture

## Task Understanding
You're constructing an axis-aligned polygon to capture mackerels while avoiding sardines.
Score = max(0, mackerels_inside - sardines_inside + 1).

## Strategy 1: Spatial Analysis
Call analyze_fish_distribution FIRST. It returns:
- Grid cells with mackerel/sardine counts
- High-density mackerel regions to target
- Low-density/sardine-poor regions to expand

## Strategy 2: Multi-Approach Search
Implement this structure in your C++ main():

```cpp
int best_score = -1;
std::vector<Point> best_poly;

// Try multiple strategies:
auto strategy_rectangles = make_rectangles();      // Simple bounding boxes
auto strategy_lobes = make_multiple_lobes();       // L-shaped, U-shaped polygons
auto strategy_gaps = expand_around_gaps();         // Grow around empty regions

for (auto& strategy : {rectangles, lobes, gaps}) {
    // Generate variants
    for (auto& poly : strategy.generate_variants(max_time_remaining)) {
        // Validate constraints
        if (!valid(poly)) continue;
        
        // Score internally with efficient counting
        int score = score_polygon(poly);
        if (score > best_score) {
            best_score = score;
            best_poly = poly;
        }
    }
}

// Output best polygon
```

## Key Constraints
- Vertices: ≤1000, all distinct, integer coords in [0, 100000]
- Perimeter: ≤400000
- Edges: strictly axis-aligned (horizontal or vertical)
- No self-intersection

## Performance Tips
- Use KD-tree (already in seed) for fast fish point queries
- Process fish in O(log N) per point for each polygon edge
- Internal scoring should be fast: O(vertices × log N) or better
- Stay well within 1.95s time limit

## When to Use Tools
- analyze_fish_distribution: ONCE at start, before any editing
- edit_solution: After each strategy iteration, or when a new approach is promising
- evaluate_solution: ONCE per promising final candidate (budget is precious!)
- probe_solution: For ranking multiple variants before full evaluation
- finish: When you've tried multiple strategies and can't improve

**Remember**: The C++ program must implement its OWN search loop! Don't just output one hardcoded polygon.
