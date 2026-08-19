You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER ANALYSIS:
   - Read all fish coordinates (N mackerels, N sardines)
   - Use coordinate-based clustering (not grid): group fish by proximity
   - Find dense mackerel clusters and sparse sardine regions

2. RECTANGLE-BUILDING STRATEGY:
   - For each mackerel cluster, find its bounding box
   - Count mackerels and sardines in this bounding box
   - If mackerels > sardines, consider this rectangle

3. COMBINING RECTANGLES:
   - Try combining adjacent rectangles with small gaps
   - Merge overlapping rectangles
   - Try unions of 2-4 rectangles to form larger polygons

4. SHAPE OPTIMIZATION:
   - Start with rectangles, then try L-shapes (union of 2 rectangles)
   - Try adding/removing edges to improve score
   - Use coordinate-based mutations: shift edges by small amounts (1-5 units)

5. VALIDATION:
   - Ensure polygon is valid: 4-1000 vertices, integer coords, no self-intersection
   - Perimeter <= 400,000

6. MULTIPLE STRATEGIES:
   - Try 5-10 different strategies with different random seeds
   - Strategies: individual rectangles, rectangle unions, L-shapes, complex polygons
   - Track best polygon across all strategies

7. TIME MANAGEMENT:
   - Use efficient O(N) or O(N log N) fish counting
   - Limit total iterations to stay under 1.9s
   - Parallelize strategy attempts

edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
evaluate_solution: Run C++ program, get score
finish: Submit when you have encoded coordinate-based clustering strategy
