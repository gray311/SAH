You are optimizing a C++ program for polygon construction.

PROBLEM: Given N mackerels and N sardines on a 2D plane, build an axis-aligned polygon (edges parallel to x or y axes) with <= 1000 vertices and perimeter <= 400000 to maximize: max(0, mackerels_inside - sardines_inside + 1).

YOUR JOB: The program outputs m vertices (coordinates). It does NOT perform any search or scoring internally. Your edits must make the C++ code produce a COMPLETE, VALID polygon specification.

SUCCESS PATTERNS TO EMBED:
- Read all fish positions first (N mackerels, then N sardines)
- Sort by x and y coordinates to identify natural "regions"
- Build a polygon that wraps high-mackerel regions, using axis-parallel edges
- Ensure vertex count <= 1000 and perimeter <= 400000
- Handle edge cases: if no good region exists, output a simple rectangle covering the origin with score 1
- Always output valid coordinate ranges (0 to 100000)

USE evaluate_solution frequently (you have ~20 evaluations). Each edit should focus on one aspect: parsing, construction, or validity checks.
