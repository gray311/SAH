You are solving an NP-hard fish-capture optimization problem.
Goal: Maximize (mackerels_inside - sardines_inside + 1) with an axis-aligned, non-self-intersecting polygon.

KEY INSIGHT: The optimal solution is NOT a single complex polygon. It is the UNION of multiple small axis-aligned rectangles, each with positive (mackerels - sardines).

YOUR TASK: Implement a RECTANGLE-DECOMPOSITION algorithm in C++:

1. Pre-process all fish into a grid or hash table for O(1) counting.

2. Enumerate candidate rectangles efficiently:
   - Consider all pairs of mackerels as potential opposite corners
   - OR use a grid-based approach: for each grid cell, compute net score
   - OR use the "maximal empty rectangle" variant: expand from each mackerel

3. For each candidate rectangle, compute its score (mackerels - sardines).

4. Greedily select rectangles with positive score, ensuring non-overlapping (or minimally overlapping).

5. Union the selected rectangles into a valid axis-aligned polygon (output vertices).

6. Optimize: You have 2.0s per evaluation. Use early termination, efficient data structures, and pruning.

CRITICAL: Each evaluation must run a complete rectangle-search algorithm, NOT a local refinement of one polygon. The search space is too large for hill climbing — use enumeration + greedy selection.

Tools:
- edit_solution: Modify C++ code to implement the rectangle-decomposition algorithm. Focus on: grid-based enumeration, efficient scoring, greedy rectangle union.
- evaluate_solution: Run and get combined_score. Use to verify algorithm correctness.
- finish: When algorithm consistently finds high-scoring unions.

Preserve EVOLVE-BLOCK markers and I/O format. Time budget is critical — optimize inner loops.
