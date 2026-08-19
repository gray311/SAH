You are an expert software developer optimizing a polygon construction algorithm.
TASK: Build an orthogonal polygon that maximizes (mackerel_count - sardine_count + 1).
APPROACH: Use ITERATIVE REFINEMENT with bounded time.
METHOD:
1. Start with a simple bounding-box polygon
2. Implement an INTERNAL TIME-BOUNDED SEARCH loop
3. Try small modifications in each iteration
4. Track best polygon within time limit
5. Output the best polygon vertices
CONSTRAINTS: Orthogonal edges, no self-intersection, 4-1000 vertices, perimeter<=400000, coords 0-100000
SEARCH: Run a WHILE loop with elapsed() check, use coordinate adjustments
