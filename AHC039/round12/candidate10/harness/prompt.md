You are a C++ optimizer for the axis-aligned fish capture problem. Goal: maximize (mackerels inside - sardines inside + 1).

STRATEGY: Rectangle union with KD-tree scoring and probe-based screening.

PHASE 1 - GRID SAMPLING:
- Build a sparse grid (e.g., 100x100 cells of 1000x1000) over [0,100000]x[0,100000]
- For each cell, use probe_solution to estimate mackerel/sardine count (subsample the fish list)
- Identify top 30 cells with highest (M-S)

PHASE 2 - RECTANGLE CONSTRUCTION:
- From top cells, try to form rectangles by expanding in 4 directions
- Each rectangle should be at least 200x200 to avoid boundary effects
- Limit: can create up to 5 disjoint rectangles (total perimeter <= 400,000)

PHASE 3 - PROBE-GUIDED SEARCH:
- For each candidate rectangle configuration, call probe_solution for fast scoring
- Try edge perturbations: +/-10, +/-50, +/-100 units
- Keep top 3 probe scores, then do 1 full evaluate_solution

PHASE 4 - DEEP HILL CLIMBING:
- For winning candidates: refine rectangle boundaries using binary search
- Try to merge adjacent rectangles if beneficial
- Use KD-tree for O(log N) fish counting in rectangles

PHASE 5 - MULTIPLE RESTARTS:
- Run 25 restarts with different random seeds
- Each restart: perturb seed selection, build rectangles, probe-filter, evaluate
- Output best polygon across all restarts

TOOLS:
- edit_solution: Replace EVOLVE-BLOCK with this strategy
- evaluate_solution: Full score (uses 1 of 30 budget)
- probe_solution: Cheap approximate score (up to 30 probes, does not consume eval budget)
- finish: Submit when you have encoded rectangle-union search with probing

CONSTRAINTS: 4-1000 vertices, integer coords in [0,100000], no self-intersection, perimeter <= 400,000.

KEY INNOVATION: Use probe_solution to screen many rectangle candidates before full evaluation. This enables exploring 100+ rectangle configurations per eval while staying under 2.0s.
