---
name: rectangle-decomposition-strategy
description: Guide C++ implementation of rectangle-decomposition algorithm for fish-capture. Enumerate candidate rectangles, score each, greedily select positive-score rectangles, union them.
---

# Rectangle-Decomposition Strategy for Fish Capture

## Problem
Maximize: mackerels_inside - sardines_inside + 1

## Key Insight
The optimal solution is a UNION of multiple small axis-aligned rectangles, each with positive net score. Not a single complex polygon!

## Algorithm Overview

### Phase 1: Fast Fish Lookup
struct Cell { int m, s; };
std::vector<Cell> grid(MAX_X / CELL_SIZE + 1, MAX_Y / CELL_SIZE + 1);

### Phase 2: Enumerate Candidates
Option A: Grid-Sweep (recommended for sparse data)
std::vector<Rectangle> candidates;
for (int cy = 0; cy < grid.size(); cy++) {
    for (int cx = 0; cx < grid[cy].size(); cx++) {
        if (grid[cy][cx].m > grid[cy][cx].s) {
            Rectangle r = expand(cell_to_rect(cx, cy));
            candidates.push_back(r);
        }
    }
}

Option B: Corner-Pair (for dense clusters)
std::vector<Rectangle> candidates;
for (auto& m : mackerels) {
    for (auto& m2 : mackerels) {
        Rectangle r({std::min(m.x, m2.x), std::min(m.y, m2.y),
                     std::max(m.x, m2.x), std::max(m.y, m2.y)});
        if (score(r) > 0) candidates.push_back(r);
    }
}

### Phase 3: Greedy Selection
std::sort(candidates.begin(), candidates.end(), 
          [](const Rect& a, const Rect& b) { return (a.m - a.s) > (b.m - b.s); });

std::vector<Rectangle> selected;
for (const auto& r : candidates) {
    if (can_add_without_negating_score(selected, r)) {
        selected.push_back(r);
    }
}

### Phase 4: Union to Polygon
- Compute union of selected rectangles
- Extract vertices of orthogonal polygon
- Output in order

### Phase 5: Time Budget
- 1.5s: enumeration + selection
- 0.5s: polygon construction + output

## Optimization Tips
- Use coordinate compression if grid too large
- Prune rectangles that are subsets of already-selected ones
- Use integer arithmetic where possible
- Early exit if total time budget exceeded
