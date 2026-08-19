You are an expert C++ algorithm engineer solving a geometric optimization problem.

Task: Construct an axis-aligned polygon (max 1000 vertices, perimeter ≤400000) to maximize (mackerels inside - sardines inside + 1).

Method — GRID-BASED POLYGON CONSTRUCTION:
1. Read all fish (5000 mackerels, 5000 sardines) and their coordinates.
2. Build a spatial grid (e.g., 100×100 or adaptive) and compute the mackerel/sardine ratio for each cell.
3. Identify high-ratio cells (e.g., ratio > 1.5 or top 30% of cells by ratio).
4. For selected cells, construct a minimal axis-aligned polygon that covers them (use bounding boxes, merge adjacent cells).
5. Ensure validity: polygon must not self-intersect, vertices distinct, perimeter ≤400000.
6. Use SEARCH/REPLACE diffs to experiment with: (a) grid resolution, (b) ratio threshold, (c) cell selection strategy (top-k by ratio, by area, etc.).
7. Always keep the fixed CPP_CODE entry point intact; only modify the internal search/construction logic inside the EVOLVE-BLOCK.

Search strategy: Run an internal loop until time limit - 0.1s. Each iteration:
- Adjust one parameter (grid size, threshold, selection method).
- Construct polygon, validate, compute score.
- Keep best score.

Critical: The internal search MUST finish well within 2.0s. Avoid O(N²) or O(N³) loops. Use KD-tree or grid cells for O(1) cell lookups.
