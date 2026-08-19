You are an expert algorithm engineer solving the "Ahc039: Efficient Fishing" NP-hard problem.

TASK: Construct an axis-aligned polygon (vertices on integer grid) that maximizes (mackerels_inside - sardines_inside).
Scoring: max(0, a - b + 1) where a=mackerels, b=sardines. Polygon must be simple, edges parallel to axes, perimeter <= 4e5, vertices <= 1000.

YOUR STRATEGY (follow exactly):
1. READ INPUT: Get fish coordinates. Separate mackerels (type 1) and sardines (type -1).
2. BUILD KD-TREE: Organize ALL fish by x-coordinate, then y-coordinate for efficient rectangular queries.
3. COMPUTE DENSITY MAP: Divide the 0-100000 grid into 50x50 cells (each 2000x2000). For each cell, compute net score = (#mackerel - #sardine).
4. FIND HIGH-VALUE REGIONS: Identify cells with positive net score. These are "profit zones".
5. CONSTRUCT POLYGON: Build an axis-aligned polygon that UNIONs the profit zones. Start with the largest connected profit zone, expand to adjacent profitable cells.
6. BOUNDED SEARCH: Within the 2s time limit, try multiple polygon constructions (rectangles, L-shapes, unions of rectangles) and pick the best.
7. VALIDATE: Ensure polygon is simple (no self-intersection) and within constraints.

TIME LIMIT: 2.0s with 0.1s safety margin. Your entire search must complete within 1.9s.
Use KD-tree for O(log N) rectangular queries. Pre-compute density once, then search polygon shapes.

OUTPUT FORMAT: Print number of vertices, then each vertex (x y) on separate lines.
