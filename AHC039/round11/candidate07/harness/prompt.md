You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL: The seed program already achieves 2.48. Your job is to IMPROVE upon it.

SEARCH METHOD (must complete in < 1.8s):

1. QUICK CLOUD ANALYSIS:
   - Read all N=5000 mackerels and N=5000 sardines
   - Compute the bounding box of all mackerels
   - Compute the centroid of mackerel positions

2. RECTANGLE SEARCH:
   - Start with the mackerel bounding box
   - Try shrinking it on each side to exclude sardines
   - For each mackerel on the boundary, try expanding that boundary
   - Score: count mackerels inside - count sardines inside + 1

3. TINY RECTANGLES AROUND CLOCKS:
   - For each mackerel, create a 50x50 rectangle centered on it
   - Score each rectangle, track top 10
   - These are fast to compute and may find high-density clusters

4. COMBINE TOP CANDIDATES:
   - Union the top 3 rectangles into a polygon
   - Ensure valid output: 4-1000 vertices, no self-intersection

5. MINIMAL HILL CLIMBING:
   - Adjust the best rectangle vertices by ±50, ±100
   - 2 iterations maximum

6. ALWAYS PRODUCE VALID OUTPUT:
   - If time runs out, output the best valid polygon found
   - Don't try to be too clever - simple rectangles often work best

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing rectangle search
- evaluate_solution: Run C++ program, get score
- finish: Submit when you beat 2.48 with a simple, fast rectangle optimizer
