You are a C++ solver for the fish polygon optimization task.
Goal: Output an axis-aligned polygon (4-1000 vertices, perimeter <= 400k) maximizing (mackerels - sardines + 1).

STRATEGY: Direct geometric envelope construction with rectangle-based refinement.

PHASE 1 - Extreme Point Detection:
- Parse all mackerel and sacker coordinates
- Find min_x, max_x, min_y, max_y among mackerels
- These define the bounding box

PHASE 2 - Rectangle Testing:
- Start with full bounding box of mackerels
- Count mackerels inside and sardines inside
- Score = mackers - sardines + 1
- If score < 1, find tightest rectangle covering at least one mackerel but excluding many sardines

PHASE 3 - Edge Refinement:
- For each edge of current rectangle(s), try shifting by small amounts
- Priority: expand towards mackerel density, contract away from sardine clusters
- Use the exact fish coordinates (not grid approximation)

PHASE 4 - Multi-Rectangle Strategy:
- If one rectangle fails, try combining 2-3 adjacent rectangles
- Each rectangle should capture a dense mackerel cluster while avoiding sardines
- Connect rectangles with thin corridors if beneficial

PHASE 5 - Output:
- Ensure valid polygon format: vertices 4-1000, integer coords [0,100000]
- Perimeter constraint: sum of edge lengths <= 400,000
- No self-intersection (axis-aligned rectangles naturally satisfy this)

CRITICAL: Work DIRECTLY with fish coordinates. Do NOT use grid abstraction.
Enumerate rectangles by testing combinations of x and y boundaries derived from fish positions.
Use both min/max and percentiles of mackerel distribution to find good boundaries.

Time budget: 2.0s per evaluation. Output valid polygon deterministically.
