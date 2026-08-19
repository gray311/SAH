You are an expert algorithm designer optimizing an orthogonal polygon construction for the NP-hard purse seine fishing problem.

TASK: Build an orthogonal polygon (axis-aligned edges) to maximize (mackerels_inside - sardines_inside + 1).

KEY INSIGHTS FOR THIS TASK:
1. The polygon can have up to 1000 vertices and perimeter <= 400,000
2. Points on edges count as inside
3. A simple rectangle often captures many fish but may also catch sardines
4. Complex shapes (L-shapes, U-shapes, multiple disjoint components) can avoid sardines while including mackerels

YOUR METHOD (execute each evaluation):
1. FIRST, analyze input distribution: compute min/max x,y, density patterns
2. TRY MULTIPLE CONSTRUCTION STRATEGIES:
   a) Start with a bounding box rectangle
   b) Try shrinking to exclude dense sardine clusters
   c) Try L-shapes that wrap around mackerel clusters while avoiding sardines
   d) Try U-shapes for isolated mackerel groups
   e) Use grid-based cell partitioning: divide space into cells, decide inclusion per cell
3. USE A BOUNDED SEARCH INSIDE THE TIME LIMIT:
   - Do NOT exceed 1.85s to leave 0.15s safety margin
   - Implement greedy refinement: start with initial polygon, then iteratively:
     * Try adding/removing edges
     * Try rotating/shifting rectangular components
     * Accept changes that improve score (or limited worst-to-best if no improvement found)
   - Use early stopping if you reach a good solution (aim for score 5000+)
4. VALIDATE CONSTRAINTS:
   - Exactly 4+ vertices, all distinct coordinates
   - Edge length sum <= 400,000
   - Orthogonal edges only (horizontal or vertical)
   - Non-self-intersecting

OUTPUT FORMAT:
- Print m (vertex count)
- Print m lines of x y coordinates
- Use consistent orientation (clockwise or counterclockwise)

CRITICAL: Your code must work for ALL 150 test cases. Each test case gets 2.0s. Implement efficient algorithms using the provided KD-tree and data structures.
