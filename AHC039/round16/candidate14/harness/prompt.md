You are a C++ polygon optimizer for the "purse seine fishing" problem.
Goal: Maximize (mackerels_inside - sardines_inside + 1).

TASK STRATEGY: Axis-aligned rectangles with gradient-based refinement.

SEARCH METHOD:

1. GRID-BASED DENSITY ESTIMATION:
   - Build 100x100 grid (cell_size=1000) over [0,100000]x[0,100000]
   - Count mackerels (M) and sardines (S) in each cell
   - Compute score = M - S for each cell

2. RECTANGLE GENERATION (key innovation vs seed):
   - Generate 20 random rectangles per restart
   - Rectangle parameters:
     * Randomly sample top 30 cells with positive M-S score as seeds
     * For each seed, try 20 rectangles with random sizes (200-800 units) and positions
     * Ensure all rectangles are within bounds [0,100000]

3. RAPID PROBE RANKING:
   - Use probe_solution to score all 20 rectangles per restart (max 600 probes total across 30 restarts)
   - Probe is cheap (~10s) and doesn't consume evaluation budget

4. DEEP HILL CLIMBING (only on top 5 probed rectangles):
   - For each of the top 5 rectangles by probe score:
     * Try edge shifts of ±5, ±10 units in each direction (8 corners × 2 shifts = 16 variants)
     * Score each variant with probe (up to 80 more probes)
     * Keep the best variant

5. FULL EVALUATION:
   - Evaluate the single best rectangle (after hill climbing) using evaluate_solution

6. MULTIPLE RESTARTS:
   - Run 30 restarts with different random seeds
   - Total: 30 restarts × 20 rectangles × 1 probe + 5 hill-climb × 8 probes + 1 eval
   - Well within 30 eval budget, ~2s time per restart

7. VALIDATION:
   - Output valid axis-aligned polygon (rectangle is a 4-vertex polygon)
   - Ensure perimeter <= 400,000 and coordinates in [0,100000]

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation of above
- evaluate_solution: Full evaluation (consumes 1 eval credit)
- probe_solution: Cheap approximate score (doesn't consume eval budget)
- finish: Submit best result

KEY DIFFERENCE from current harness: Use simple rectangles instead of complex multi-lobed structures, leverage probe_solution for rapid ranking, focus on fewer high-quality candidates.
