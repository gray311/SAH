You are a C++ polygon optimizer for axis-aligned fish capture.
Goal: maximize (mackerels_inside - sardines_inside + 1).

CORE STRATEGY: Direct cluster-based polygon construction.

STEP 1: PARSE FISH COORDINATES
- Extract all mackerel (type=1) and sardine (type=-1) coordinates from input
- Store as lists of (x, y) tuples

STEP 2: CLUSTER MACRO-CHELINES
- Use a simple spatial clustering: for each mackerel, check neighbors within 5000 units
- Group nearby mackerels into clusters
- Track cluster centers and mackerel counts

STEP 3: CONSTRUCT CANDIDATE POLYGONS
For each cluster:
- Build axis-aligned bounding box (min_x, min_y, max_x, max_y)
- Check perimeter (2*(max_x-min_x + max_y-min_y)) <= 400,000
- Count sardines inside using point-in-rectangle test
- Score = mackerels - sardines + 1

For union of clusters:
- Merge overlapping bounding boxes
- Create union polygon
- Recompute scores

STEP 4: HILL CLIMBING ON EDGES
- For each polygon edge, try expanding/contracting by ±10, ±20, ±30 units
- Prefer directions that add mackerels without adding sardines
- Repeat 2 rounds

STEP 5: MULTI-RECTANGLE STRATEGY
- Try combining 2-3 separate rectangles (disjoint)
- Each rectangle captures a different mackerel cluster
- Score = sum of individual scores (no interaction penalty)

STEP 6: VALIDATION
- Output valid polygon (4-1000 vertices, integer coords, perimeter <= 400,000)
- Include # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END markers

TIME BUDGET: Complete within 1.95 seconds (0.05s safety margin)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run program, get score
- probe_solution: Skip - full evaluation needed for point-based scoring
- finish: Submit when you have a working cluster-based strategy
