You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Bounding-box exploration with KD-tree spatial queries.

CORE APPROACH:
1. Load all fish positions from input
2. Use existing KD-tree structure for fast spatial queries
3. Explore promising bounding boxes by:
   - Computing bounding box of ALL mackerels as initial candidate
   - Systematically expand/shift bounding box boundaries
   - For each candidate, query mackerel count and sardine count in the rectangle
   - Track best score: M - S + 1

SEARCH LOOP (must run until time budget ~1.9s):
- Start with the full mackerel bounding box
- Try shrinking from each edge inward (10, 20, 50, 100 unit increments)
- Try expanding mackerel bounding box in each direction
- Try centered rectangles that cover different density regions
- For promising candidates, do local refinement (small boundary adjustments)
- Use KD-tree rectangle queries for fast scoring

POLYGON OUTPUT:
- Output a simple axis-aligned rectangle (4 vertices) for most candidates
- Ensure valid: 4-1000 vertices, integer coords [0,100000], perimeter ≤ 400,000

TIME MANAGEMENT:
- Generate multiple candidate polygons (20-50 variants) per evaluation
- Output the one with highest score
- Prioritize quantity over complexity to explore more regions
- Use KD-tree O(log N) queries for fast rectangle scoring

VALIDATION: Always output valid polygon format: m\n a_0 b_0 \n ... \n a_{m-1} b_{m-1}
Every test case must produce valid output.
