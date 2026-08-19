You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

TASK UNDERSTANDING:
- N=5000 mackerels and 5000 sardines at distinct integer coordinates in [0,100000]x[0,100000]
- Build an axis-aligned polygon (4-1000 vertices, perimeter <= 400,000)
- Score = (#mackerels inside) - (#sardines inside) + 1
- Points on edges count as inside

CRITICAL SEARCH STRATEGY (uses KD-tree for fast rectangle scoring):

PHASE 1: BOUNDARY SEARCH
- Start with a minimal bounding box around ALL fish (or a heuristic initial box)
- Use KD-tree to count mackerels/sardines in current polygon O(log N) per query

PHASE 2: VERTEX REFINEMENT (key innovation)
- For each vertex of the polygon, try small integer perturbations:
  * For horizontal edges: shift y-coordinate by ±1, ±2, ±3, ±4, ±5
  * For vertical edges: shift x-coordinate by ±1, ±2, ±3, ±4, ±5
  * For each perturbation, query KD-tree for new score
  * Keep perturbation that maximizes score
- Repeat for all vertices until no improvement

PHASE 3: CORNER ADJUSTMENT
- Try adding/removing corners to create more complex shapes:
  * Split a long edge into two with a small corner
  * Merge adjacent corners if redundant
- Use KD-tree to score each variation

PHASE 4: MULTI-LOBED CONSTRUCTION
- Identify separate high-density mackerel regions (via KD-tree range queries)
- Build separate rectangular "lobes" around each region
- Connect lobes with minimal perimeter cost

PHASE 5: VALIDATION & OUTPUT
- Ensure polygon is simple (no self-intersection)
- Verify vertex count (4-1000) and perimeter constraint
- Use integer coordinates only
- Output in required format: m\nx0 y0\n...\n\n\n  IMPLEMENTATION NOTES:
- Use the seed's KD-tree infrastructure (it's efficient and accurate)
- KD-tree queries are fast enough to do hundreds per second
- Focus search on regions with high mackerel density and low sardine density
- Start with a simple rectangle, then iteratively refine
- Total iterations per eval: 50-100 (fits in 2s time limit)

TOOLS:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing this KD-tree based vertex refinement strategy
- evaluate_solution: Run C++ program, get score (mackerels-sardines+1)
- probe_solution: NOT useful - KD-tree scoring is accurate and fast
- finish: Submit when you have a working KD-tree based optimization
