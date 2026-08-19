You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

GEOMETRIC STRATEGY (coordinate-based, not grid-based):

1. PARSE FISH COORDINATES:
   - Read all mackerel and sardine coordinates from input
   - Store in sorted arrays for fast query

2. BUILD MACKEREL CLUSTERS:
   - Find mackerels within 5000 units of each other
   - Create tight bounding boxes around each cluster

3. REFINED RECTANGLE SEARCH:
   - For each cluster bounding box, try expanding coordinates by ±100, ±200, ±500 units
   - Count mackerels and sardines in each candidate rectangle
   - Score = mackerels - sardines + 1

4. COMBINATORIAL MERGING:
   - Try merging adjacent rectangles (union of two boxes)
   - For 3-4 rectangle unions, ensure valid simple polygon

5. LOCAL OPTIMIZATION:
   - For promising rectangles, try edge shifts of ±50, ±100, ±200, ±500 units
   - Accept only if score improves

6. MULTIPLE RESTARTS:
   - Run 10-15 restarts with different cluster selections
   - Each restart: pick 2-3 mackerels, build bounding box, refine

7. VALIDATION:
   - Output 4-1000 vertices, perimeter ≤ 400,000, coords in [0,100000]
   - For rectangles: 4 vertices; for merged shapes: compute convex hull or custom polygon

Tools:
- edit_solution: Replace EVOLVE-BLOCK with this coordinate-based strategy
- evaluate_solution: Run and get score
- probe_solution: NOT useful for this geometric search
- finish: Submit when you have working rectangles
