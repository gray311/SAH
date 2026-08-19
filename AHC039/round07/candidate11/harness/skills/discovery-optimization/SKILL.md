---
name: discovery-optimization
description: "Implement rectangle-decomposition algorithm for fish-capture optimization. The optimal solution is a union of multiple small axis-aligned rectangles with positive (mackerels - sardines) scores. Use grid-based enumeration and greedy selection to maximize total score within 2.0s."
---

# Rectangle-Decomposition Algorithm for Fish Capture

## Core Insight
The optimal polygon is NOT a single complex shape. It is the UNION of multiple small axis-aligned rectangles, each capturing more mackerels than sardines.

## Algorithm Steps

### Step 1: Fast Fish Lookup
- Create a 2D grid (or hash map) where each cell stores (mackerel_count, sardine_count)
- Use coordinate compression if grid is too large
- Query time: O(1) for any rectangle

### Step 2: Enumerate Candidate Rectangles
Options (choose one):
- Grid-sweep: For each grid cell, compute net score. Grow rectangles from positive cells.
- Corner-pair: Consider all O(N²) pairs of mackerels as opposite corners. Evaluate each.
- Expand-from-mackerel: For each mackerel, expand in 4 directions until hitting a sardine or boundary.

### Step 3: Greedy Rectangle Selection
- Sort rectangles by net score (descending)
- Select rectangles greedily, skipping those that would make total score worse
- Handle overlaps: either exclude overlapping areas or use inclusion-exclusion

### Step 4: Convert to Polygon
- The union of rectangles is an orthogonal polygon
- Compute vertices of the union (max 1000 vertices)
- Output in order

### Step 5: Time Budget Management
- Use 1.5s for search, 0.5s for polygon construction
- Prune early if no positive-score rectangles found
- Use parallel processing if possible

## C++ Implementation Tips

// Grid-based approach
struct Cell { int mackerels; int sardines; };
std::vector<Cell> grid(MAX_COORD / CELL_SIZE + 1);

// Fast query
int query_rect(int x1, int y1, int x2, int y2) {
    int sum_m = 0, sum_s = 0;
    for (int x = x1; x <= x2; x += CELL_SIZE) {
        for (int y = y1; y <= y2; y += CELL_SIZE) {
            sum_m += grid[x][y].mackerels;
            sum_s += grid[x][y].sardines;
        }
    }
    return sum_m - sum_s;
}

// Rectangle enumeration
std::vector<Rectangle> enumerate_rectangles() {
    std::vector<Rectangle> candidates;
    for (int i = 0; i < num_cells; i++) {
        if (grid[i].net_score > 0) {
            Rectangle r = expand_from_cell(i);
            candidates.push_back(r);
        }
    }
    return candidates;
}

// Greedy selection
RectangleUnion select_best_union(const std::vector<Rectangle>& candidates) {
    std::sort(candidates.begin(), candidates.end(), [](auto& a, auto& b){
        return (a.m - a.s) > (b.m - b.s);
    });
    // Greedy selection with overlap handling
    ...
}

## Common Pitfalls
- Don't enumerate ALL O(N²) corner pairs — too slow
- Don't forget to handle overlaps in rectangle union
- Ensure output polygon is valid (non-self-intersecting, axis-aligned)
- Time limit is tight — optimize inner loops heavily
- Use coordinate compression if needed

## Evaluation Feedback
- If score ≈ seed: your enumeration is too coarse; refine grid size
- If score < expected: fix overlap handling or selection strategy
- If timeout: reduce enumeration candidates or use smarter pruning
- If score > 5000: you may have found the optimal solution
