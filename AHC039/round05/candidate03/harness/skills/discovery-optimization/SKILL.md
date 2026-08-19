---
name: discovery-optimization
description: "Solve geometric polygon construction problems with greedy expansion strategies. You have 20 evals and 150 test cases - optimize for speed per case."
---

# Greedy Polygon Growing Algorithm
## Problem Maximize: mackerels inside polygon - sardines inside polygon Score: max(0, captured_mackerels - captured_sardines + 1)
## Strategy: Greedy Expansion from Bounding Box
### Algorithm Overview 1. Parse input: N mackerels + N sardines 2. Start with bounding box covering ALL mackerels 3. For 100-300 iterations: - Try expanding polygon in 4 cardinal directions - Each expansion: push one edge outward by delta - Score each candidate polygon (quick rectangle-point inclusion) - Keep best improvement 4. Output final polygon
### Key Implementation Details
Point Inclusion: A point (x,y) is inside rect [(x1,y1),(x2,y2),(x2,y3),(x1,y3)] iff: x1 <= x <= x2 AND y1 <= y <= y3
Score Function: O(n) per call - iterate all points, count those inside polygon
Efficient Expansion: - Maintain current poly as 4 coordinates (x_min, x_max, y_min, y_max) - Try: expand x_min by -delta, x_max by +delta, y_min by -delta, y_max by +delta - For irregular polygons, track each edge position
Optimization: - Pre-sort mackerels/sardines by x and y coordinates - Use this for fast range queries during expansion search - Or: precompute for each point its bounding box contribution
Timeline for 150 test cases in 2 seconds: - You need ~0.013 seconds per test case - Parsing: 5ms - Main loop: 200 iterations - Each iteration: 4 directions x 4 deltas = 16 candidate scores - Each score: ~5000 point checks = 80k ops - Total: 200 x 16 x 80k = 256M ops -> tight but doable in C++
Better approach: Limit to 50 iterations, or use approximate scoring (sample points)
Sample C++ Structure: int N = read(); vector<Point> mackerel(N), sardine(N); for(int i=0;i<N;i++) cin >> mackerel[i].x >> mackerel[i].y; for(int i=0;i<N;i++) cin >> sardine[i].x >> sardine[i].y;
bounding box: int mx_min = inf, mx_max = -inf, my_min = inf, my_max = -inf; for(auto& p : mackerel) { mx_min=min(mx_min,p.x); mx_max=max(mx_max,p.x); /*...*/ }
Greedy expansion loop: for iteration in 100..300: best_score = score(poly, mackerels, sardines) for dir in [N, S, E, W]: for delta in [1, 10, 50, 100]: cand_score = score(expanded_poly, mackerels, sardines) keep if better
## Output Format 4 0 0 100000 0 100000 100000 0 100000
(Example: rectangle covering entire space)
