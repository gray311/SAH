You are optimizing an orthogonal polygon (edges parallel to x/y axes) that maximizes:
score = (mackerels inside) - (sardines inside) + 1, clamped at 0.

Key constraints:
- Polygon must be non-self-intersecting
- Vertices must be integer coordinates in [0, 100000]
- Max 1000 vertices, max perimeter 400000

STRATEGY: Use multiple short evaluations to explore candidate polygons.
Don't try to find the optimal polygon in one shot. Instead:
1. Generate several candidate polygon shapes (rectangles, L-shapes, rectangles with cuts)
2. Use probe_solution to quickly rank candidates on subsampled data
3. Pick the best candidate and run a FULL evaluate_solution
4. Iteratively refine: add/remove cuts, shift boundaries, merge/split regions

Always call probe_solution FIRST to filter promising candidates before spending evaluation budget.
If probe says a candidate is bad, discard it immediately.
If you see score is plateauing, try fundamentally different shapes (e.g., if rectangles fail, try multi-region polygons).

Track your best full score carefully. Never trust probe scores as final - always confirm with evaluate_solution.
