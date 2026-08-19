You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).
CORE STRATEGY: Bounding Box Edge Refinement
Instead of complex corridor expansion, use simple bounding box refinement:
1. FIND CORE REGION: - Parse fish positions from input - Find bounding box that captures most mackerels with minimal sardine penalty - Start with a conservative box around mackerel cluster
2. EDGE-LEVEL OPTIMIZATION: - For each of the 4 edges (top, bottom, left, right): * Try shifting edge by ±1, ±2, ±3, ±4, ±5 units * Count mackerels/sardines gained/lost for each shift * Keep the shift that maximizes (mackerels - sardines) - Repeat for all 4 edges
3. ITERATIVE IMPROVEMENT: - After optimizing all 4 edges, repeat the process - Continue until no improvement in 2 consecutive rounds
4. MULTIPLE RESTARTS: - Run 10 restarts with different starting boxes - Each restart: pick random point as seed, expand to capture nearby mackerels, then refine edges - Output best polygon across all restarts
5. VALIDATION: - Ensure 4-1000 vertices, integer coordinates in [0,100000] - Perimeter ≤ 400,000 - Output valid polygon: m then m vertices
Key insight: Simple bounding box refinement with local edge optimization works better than complex multi-lobed structures for this task.
