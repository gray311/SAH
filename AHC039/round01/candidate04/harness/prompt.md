You are an expert C++ developer optimizing a geometric packing algorithm.
Task: Find an axis-aligned polygon maximizing (mackerels_inside - sardines_inside + 1).

CRITICAL: Implement a TIME-BASED INTERNAL SEARCH LOOP inside your code.
The evaluator gives you 2.0 seconds per test case. Your program MUST:
1. Start with a seed polygon (e.g., bounding box or simple shape)
2. Loop: (a) evaluate current score, (b) generate a modified polygon, (c) if improved, keep it
3. Continue until time expires or no improvement in 100 iterations

SEARCH STRATEGY:
- Use greedy: grow polygon outward to capture nearby mackerels
- Or use local search: randomly perturb one vertex, keep if score improves
- Or use divide-and-conquer: partition grid into regions, optimize each

PERFORMANCE: You have 20 evaluations total, 150 test cases. Spend ~8s on search to pass all 150.
Don't be greedy-only — use internal iteration to improve from seed.

The EVOLVE-BLOCK contains CPP_CODE. Only edit that region. Preserve the fixed entry function.
