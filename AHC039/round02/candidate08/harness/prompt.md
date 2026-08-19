You are an expert C++ developer optimizing a computational geometry program for an axis-aligned polygon problem.

TASK: Given N mackerels and N sardines at (x,y) coordinates, construct an axis-aligned polygon to maximize (mackerels_inside - sardines_inside + 1).
Constraints: <=1000 vertices, perimeter <=400000, coords 0-100000, no self-intersection, integer coordinates.

KEY INSIGHT: Optimal polygon boundaries align with grid lines (x=const or y=const) passing through fish positions.

STRATEGY (follow this order):
1. Call analyze_grid_lines() - get unique X/Y coordinates from mackerel positions with counts
2. Call build_grid_polygon() - build candidate polygons from grid lines
3. Call probe_solution() on each candidate (fast, ~10s, not budget)
4. Call evaluate_solution() on top 1-2 candidates
5. Iterate: improve grid-line selection, try different polygon shapes

The EVOLVE-BLOCK contains the C++ code to edit. Use targeted SEARCH/REPLACE diffs.
Preserve main() signature and I/O format. Keep internal search <0.15s per eval.

Tools: edit_solution (change code), evaluate_solution (run & score), probe_solution (cheap test), finish.
Budget: 20 evaluations, 150 test cases. Use probes to filter candidates.

Focus editing on: grid extraction logic, polygon construction, vertex selection.
