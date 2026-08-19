You are solving a competitive programming task: construct a rectilinear polygon that maximizes (mackerels captured - sardines captured). N=5000 each. Score = max(0, a - b + 1).
You have 150 test cases and 20 evaluation budget. Time per eval: ~2 seconds.
KEY ALGORITHM: Implement a greedy polygon growing strategy in main(): 1. Parse all points from stdin (first N mackerels, next N sardines) 2. Start with a bounding box around ALL mackerels 3. Iteratively try expanding the polygon in 4 directions (N/S/E/W) that adds mackerels while avoiding/adding sardines 4. Run 100-300 iterations per test case before outputting final polygon
Each iteration should: - Try 4-8 candidate expansions (slide edges outward by 1-100 units) - Use KD-tree or sorted lists to quickly query points in expanded region - Score each candidate (approximate count with rectangle inclusion) - Keep best improvement
CONSTRAINTS: - Coordinates 0-100000, integer - Perimeter <= 400000 (easy with 400+ vertices) - Use consistent winding (clockwise) - Output exactly: count then vertices in order
The evaluator checks validity strictly. Your internal search can be as complex as you want as long as it stays under 2 seconds per test case.
PSEUDO-CODE STRUCTURE FOR main(): for each test case: read N, then 2N points mackerels = points[0:N] sardines = points[N:2N] mx_min, mx_max, my_min, my_max = bounds(mackerels) poly = [(mx_min, my_min), (mx_max, my_min), (mx_max, my_max), (mx_min, my_max)]
for iteration in 100..300: best_score = score(poly, mackerels, sardines) best_poly = poly
for dir in [N, S, E, W]: for expansion in [1, 10, 50, 100]: cand_poly = expand_in_direction(poly, dir, expansion) if valid(cand_poly): cand_score = score(cand_poly, mackerels, sardines) if cand_score > best_score: best_score = cand_score best_poly = cand_poly
poly = best_poly
output best_poly
Edit your EVOLVE-BLOCK to implement this strategy. Focus on making the internal loop efficient enough for 150 cases in 2 seconds each.
