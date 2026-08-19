---
name: discovery-optimization
description: "Optimize C++ code for axis-aligned fish capture polygon. Focus on efficient rectangle enumeration and KD-tree based counting. Target single rectangle or small union of 2-3 rectangles as optimal structure. Avoid complex L-shapes."
---

Fish Capture Polygon Optimization - Rectangle Strategy

Problem:
- N=5000 mackerels, N=5000 sardines at distinct integer coordinates
- Maximize: mackerels_inside - sardines_inside + 1
- Axis-aligned polygon, max perimeter 400,000

Optimal Strategy: Rectangle-Based Search

Why Rectangles Work Best:
- Simple to implement correctly in C++
- Fast to count fish with KD-tree or grid
- Often achieve near-optimal scores for this problem type
- Complex shapes add implementation difficulty without guaranteed benefit

Step-by-Step Approach:

Step 1: Build Spatial Index (50-100ms)
- Construct KD-tree for O(log N) point queries
- Alternative: 2D grid with cell-based counting
- This enables fast score computation for many candidates

Step 2: Enumerate Candidate Rectangles (500-1500ms)
- Extract unique x-coordinates from mackerels as potential boundaries
- Extract unique y-coordinates from mackerels as potential boundaries
- Generate candidate rectangles by combining x-left, x-right, y-bottom, y-top
- Focus on rectangles that enclose dense mackerel clusters
- Try both individual rectangles and unions of 2 rectangles

Step 3: Score Each Candidate (100-200ms each)
- Query KD-tree for fish inside rectangle
- Score = mackerel_count - sardine_count
- Track best score and corresponding rectangle

Step 4: Refine Best Candidate (100-300ms)
- Try small expansions/shrinks of best rectangle
- Try flipping axes if score improves
- Check perimeter constraint before accepting

C++ Implementation Patterns:

Fast rectangle scoring with KD-tree:
long long score_rectangle(const vector<Point>& rect, const KDNode* tree) {
    vector<int> mackerels, sardines;
    query_kdtree_rectangle(tree, rect.left, rect.right, rect.bottom, rect.top, mackerels);
    // Separate counts and return mackerels - sardines
}

Generate candidate rectangles from coordinate quantization:
vector<tuple<int,int,int,int>> generate_candidates(const vector<Point>& mackerels) {
    // Get unique sorted x and y coords
    // Generate all combinations of 4 points forming a rectangle
    // Return top candidates by mackerel density
}

Union of two rectangles (top-left + bottom-right corners):
vector<Point> make_union_rects(int xl1, int xr1, int yb1, int yt1,
                                int xl2, int xr2, int yb2, int yt2) {
    // Construct 8-vertex polygon representing union
    // Ensure non-self-intersecting
}

Critical Implementation Notes:

- NEVER hardcode a single rectangle - must search
- Use time-based loops with 2.0s hard limit
- Validate perimeter and vertex count before output
- Prefer simpler rectangles over complex shapes
- Output the last valid polygon (only last one is scored)

Common Mistakes to Avoid:

- Not using spatial indexing (O(N^2) scoring is too slow)
- Hardcoding polygon vertices instead of searching
- Creating self-intersecting polygons
- Exceeding perimeter limit
- Not separating mackerel and sardine counts correctly
- Outputting only 4 vertices when complex shape needed

Search Loop Template:

Initialize best_score = -inf, best_rect = null

For each candidate rectangle (enumerated systematically):
    score = count_fish_in_rect(rect)
    if score > best_score:
        best_score = score
        best_rect = rect

If time remaining > 0.1s:
    For each axis (x, y):
        For delta in [-10, -5, 5, 10]:
            candidate = expand_contract(best_rect, axis, delta)
            if valid_and_improves(candidate):
                best_rect = candidate

Output best_rect as 4-vertex polygon
