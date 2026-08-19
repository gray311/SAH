You are a C++ polygon optimizer for axis-aligned fish capture (maximize mackerels - sardines + 1).

CORE STRATEGY: Try multiple explicit polygon patterns with local edge refinement.

1. SPATIAL SETUP: Use 100x100 grid (cell_size=1000) for O(1) rectangle queries. Build grid at startup.

2. PATTERN GENERATION: For EACH of these patterns, generate candidates:
   - RECTANGLE: Find best bounding box around a 5x5 cell window
   - L-SHAPE: Two connected rectangles forming an L, parameterized by corner position
   - U-SHAPE: Three rectangles forming a U, exclude one side
   - STEPPED: Sequence of up/down steps, parameterized by step height/width
   - TIGHT-BOX: For each high-density cell, tight box around its fish

3. FOR EACH PATTERN:
   - Sample 20-30 random instances
   - For each instance, do local edge optimization: try shifting each edge by -20 to +20 (step 5)
   - Keep best valid polygon per pattern

4. OUTPUT: The single best polygon across all patterns

CRITICAL: Code must include all pattern generators, grid-based scoring, and local optimization loops. Time budget: ~1.5s for search, 0.5s margin. Preserve EVOLVE-BLOCK markers and exact I/O format (m then m vertices).
