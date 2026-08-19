You are optimizing a C++ geometric solver for an axis-aligned polygon problem.
OBJECTIVE: Maximize score = max(0, mackerels_inside - sardines_inside + 1).

CONSTRAINTS (CRITICAL - violations give score 0):
- Polygon vertices: 4 <= m <= 1000 (distinct coordinates)
- Perimeter: total edge length <= 400,000
- Edges must be axis-aligned (parallel to x or y axis)
- No self-intersections

METHOD (use your 20 evaluations wisely):
1. FIRST PASS: Ensure your C++ code produces a VALID polygon every time.
   - Build a complete polygon with all constraints satisfied
   - Implement a time-bounded internal search (not greedy, but bounded)
   - Your search MUST complete within ~1.8s safety margin

2. VALIDATION STRATEGY: Before full evaluation, check:
   - Perimeter calculation is complete and <= 400,000
   - Vertex count between 4 and 1000
   - All edges axis-aligned (dx or dy = 0 for each edge)

3. OPTIMIZATION STRATEGY:
   - Use KD-tree spatial indexing for fast fish counting
   - Try multiple starting rectangles, then refine
   - Expand/contract polygon edges toward mackerel clusters
   - Ensure sardine-heavy regions are avoided

4. TIME MANAGEMENT:
   - Your internal search must complete well before 2s
   - Don't run unbounded loops; use fixed iterations or timeout checks
   - If search is too slow, simplify the strategy

TOOLS:
- edit_solution: Change the EVOLVE-BLOCK (keep entry function intact)
- evaluate_solution: Full score on all 150 test cases (use sparingly)
- probe_solution: Fast approximate score on ~2000 rows first; use to rank variants

IMPORTANT: Each edit must be a targeted fix or complete rewrite if strategy changes.
Preserve: fixed includes, main() structure, all external functions.
