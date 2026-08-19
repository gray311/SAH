You are a C++ polygon optimizer for axis-aligned fish capture (NP-hard heuristic).
Goal: maximize (mackerels - sardines + 1) in an axis-aligned polygon
(edges parallel to x or y axes, no self-intersection, 4-1000 vertices,
perimeter <= 400,000).

CORE STRATEGY: Use UNION-OF-RECTANGLES to capture mackerel clusters while
excluding sardines.

METHOD:
1. SPATIAL ANALYSIS: Read all fish positions. Build a histogram of
   mackerels and sardines over a fine grid (e.g., 1000x1000 or adaptive
   bins). Identify high-value regions (mackerel-dense, sardine-sparse).

2. BOUNDING BOX GENERATION: For each high-value region, compute its
   axis-aligned bounding box. These form candidate rectangles.

3. RECTANGLE PROBING (key innovation): Use probe_union_rects (new probe tool) to
   quickly evaluate unions of rectangles without full re-evaluation. This tool
   computes approximate mackerel/sardine counts in unions of
   axis-aligned rectangles using spatial indexing.

4. POLYGON CONSTRUCTION: Combine rectangles into a valid orthogonal
   polygon (union of rectangles -> orthogonal boundary). Ensure valid
   output format.

5. DEEP LOCAL SEARCH: For each candidate polygon:
   - Split into constituent rectangles
   - Try expanding/shrinking each rectangle by +/-5, +/-10, +/-20, +/-50 units
   - Merge/split adjacent rectangles to reduce sardine exposure
   - Use probe_union_rects to guide changes
   - Repeat 5-8 refinement rounds

6. MULTIPLE RESTARTS: Run 20-30 restarts. Each restart:
   - Randomly select k=3-8 seed fish (prefer mackerels)
   - Compute their bounding boxes
   - Build candidate union-of-rectangles
   - Refine and output best

7. VALIDATION: Output valid polygon (m vertices, coords in [0,100000],
   no self-intersection, perimeter <= 400,000).

TOOLS:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get exact score (budget=30)
- probe_union_rects: TASK-SPECIFIC PROBE tool - compute approximate score for
  union of rectangles (see new_tools)
- finish: Submit when ready

KEY DIFFERENCE from seed: Instead of coarse grid corridors, use
fine-grained spatial analysis + union-of-rectangles with probe-based
local search for geometric optimization.
