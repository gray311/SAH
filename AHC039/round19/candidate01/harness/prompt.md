You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The current grid-based approach failed catastrophically. Use a DIRECT MINIMAL POLYGON approach instead:

SEARCH METHOD:

1. PARSE FISH DATA DIRECTLY from input (2N lines: first N mackerels, next N sardines)

2. BUILD MINIMAL POLYGON around all mackerels:
   - Create bounding box of all mackerel positions
   - If all mackerels are collinear, use the next larger configuration
   - This guarantees a valid polygon containing all mackerels

3. REFINE WITH LOCAL SEARCH:
   - For each edge of the bounding box, try expanding outward to capture more mackerels while avoiding sardines
   - Try perturbations of edge coordinates: ±10, ±20, ±30 units
   - Use edit_solution to generate candidates and evaluate_solution to score them
   - Keep improvements for 3 rounds of hill climbing

4. HANDLE EDGE CASES:
   - If mackerels are in a single row or column, expand to 2D (±1 unit perpendicular)
   - If mackerels form a single point, expand to a small square
   - Always ensure 4 <= vertices <= 1000 and perimeter <= 400,000

5. MULTIPLE RESTARTS:
   - Run 5 restarts with different random perturbations
   - Each restart: slightly perturb mackerel coordinates (±1 unit), rebuild bounding box, refine
   - Track best polygon across all restarts

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing minimal polygon approach
- evaluate_solution: Run C++ program, get score (budget=30)
- finish: Submit final solution

preserve EVOLVE-BLOCK markers, exact I/O format (m then vertices), ensure <2.0s execution.
KEY DIFFERENCE: Use direct minimal bounding box approach instead of grid-based corridor expansion.
