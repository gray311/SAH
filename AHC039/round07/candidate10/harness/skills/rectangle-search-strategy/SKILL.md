---
name: rectangle-search-strategy
description: Find optimal axis-aligned rectangle for fish capture by enumerating candidates from mackerel coordinates and scoring with fast counting.
---

Rectangle-Based Fish Capture Strategy

Why This Works:
For axis-aligned polygons, a single rectangle often achieves near-optimal scores.
Complex shapes add implementation complexity without guaranteed benefit.

Step-by-Step Implementation:

Step 1: Coordinate Quantization
vector<int> unique_x, unique_y;
for (const auto& f : mackerels) {
    unique_x.push_back(f.p.x);
    unique_y.push_back(f.p.y);
}
sort(unique_x.begin(), unique_x.end());
unique_x.erase(unique(unique_x.begin(), unique_x.end()), unique_x.end());
// Same for y

Step 2: Generate Candidate Rectangles
vector<Rect> candidates;
for (auto xl : unique_x) {
    for (auto xr : unique_x) {
        if (xl >= xr) continue;
        for (auto yb : unique_y) {
            for (auto yt : unique_y) {
                if (yb >= yt) continue;
                // Check if rectangle is valid (perimeter, area)
                candidates.push_back({xl, xr, yb, yt});
            }
        }
    }
}

Step 3: Fast Scoring with KD-Tree
int score_rect(const Rect& r) {
    vector<int> macks, sardines;
    query_kdtree(macks, r.x_left, r.x_right, r.y_bottom, r.y_top);
    return macks.size() - sardines.size();
}

Step 4: Time-Bounded Search
auto start = chrono::steady_clock::now();
double elapsed = 0;
Rect best_rect;
int best_score = -1000000;

while (elapsed < 1.9 && !candidates.empty()) {
    // Process next batch of candidates
    // ...
    elapsed = chrono::duration_cast<chrono::duration<double>>(
        chrono::steady_clock::now() - start).count();
}

Key Insights:

- Coordinate quantization reduces search space from infinite to O(N^4) candidates
- KD-tree queries enable fast O(log N) scoring per candidate
- Time budgeting ensures completion within 2.0s
- Simple is better - single rectangles often optimal

Optimization Tips:

- Skip candidates with negative mackerel count (impossible)
- Sort candidates by mackerel density first
- Early termination if score stops improving for 100 candidates
- Consider unions of 2 rectangles if single rectangle not optimal
