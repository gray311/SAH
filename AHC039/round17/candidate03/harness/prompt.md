You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).
The input has N=5000 mackerels and N=5000 sardines on [0,100000]^2. Output a valid axis-aligned polygon.

CRITICAL FAILURE DIAGNOSIS: The previous harness (grid-based with 200x200 cells and corridor expansion)
scores 2.48436 — the seed score — meaning NO improvement was found across 8 candidate harnesses.
This indicates the grid abstraction is too coarse (cell_size=500 misses fine-grained fish patterns)
and the corridor strategy fails to find improving polygons. The grid-based approach cannot
navigate local variations in fish density.

NEW STRATEGY: Direct point-based sweep-line enumeration of candidate rectangles and L-shapes.
The polygon can be up to 1000 vertices with perimeter 400,000. Use multiple passes:
1. QUICK PASS: Generate 10-20 candidate bounding boxes from random coordinate samples, then refine
2. DEEP PASS: For top candidates, enumerate all axis-aligned rectangles aligned to mackerel/sardine
   coordinates (O(mn) in worst case but with pruning), then expand to L-shapes and T-shapes
3. HILL CLIMB: For each candidate, perform local edge refinement by testing small coordinate shifts

SEARCH ALGORITHM DETAILS:
- Parse fish coordinates into sorted lists by x and y
- Candidate 1: Enumerate small bounding boxes (≤20 vertices) by trying combinations of 20 random
  x-coordinates and 20 random y-coordinates
- Candidate 2: Use coordinate compression on fish points to identify promising grid lines, then
  enumerate rectangles from these grid lines
- Candidate 3: Try L-shaped polygons formed by combining two overlapping rectangles
- For each candidate polygon, compute score by checking which fish points are inside (point-in-polygon test)
- Keep best polygon from all candidates

TIME MANAGEMENT: Distribute time across 10-15 candidate polygons, spending 0.05-0.1s each.
If time is tight, focus on the first 5-10 candidates with best bounds.

VALIDATION: Ensure 4 ≤ vertices ≤ 1000, integer coordinates in [0,100000], no self-intersection.

TOOLS:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing the point-based sweep-line enumeration
- evaluate_solution: Run C++ program and get score
- finish: Submit best solution found
