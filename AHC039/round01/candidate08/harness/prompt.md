You are an expert C++ developer optimizing an axis-aligned polygon construction for a fish-catching task.

Task: Construct a polygon (max 1000 vertices, perimeter ≤ 4×10⁵) to maximize (mackerels - sardines + 1).
- Points on edges count as inside.
- Must be simple (no self-intersections), axis-aligned edges.

Strategy: Implement a constructive algorithm that greedily builds a polygon, then performs
bounded local optimization within the time limit (leave 0.1s safety margin).

Key tactics:
1. Compute bounding box of all fish first.
2. Greedily expand outward from a starting rectangle, adding edges to enclose regions
   with net-positive fish value (more mackerels than sardines).
3. Use a simple grid-scan or distance-based heuristic to find high-value corners.
4. After construction, run 100-200 iterations of local swaps: try moving each vertex
   by ±1/2/3 units and keep improvements.
5. Ensure output format: first line = vertex count, then vertices.

Preserve the fixed entry function and all imports outside the EVOLVE-BLOCK.
Make the program compile and run within 1.9s on all test cases.
