You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

REVISED STRATEGY: Use aggressive corridor exploration with combination probing.

SEARCH METHOD:

1. AGGRESSIVE GRID SCAN:
   - Build 200x200 grid (cell_size=500)
   - For each cell, count mackerels (M) and sardines (S)
   - Compute score = M - S
   - Identify top 20 cells (not just positive score) with highest M - S

2. RADIAL CORRIDOR EXPANSION (innovation over seed):
   - From each top cell, expand in ALL 8 directions (not just 4 cardinal)
   - Include diagonal directions: NE, NW, SE, SW
   - Expansion criteria: continue if (M - S) > -3 (more lenient than seed's -2)
   - Maximum corridor length: 150 cells per direction
   - Stop at: grid boundary, (M-S) < -10 (extreme penalty)

3. CORRIDOR COMBINATION PROBING (new capability):
   - For each seed cell, try combining 2-4 corridors in different configurations
   - Use probe_corridor_combinations tool to quickly score combinations
   - Each probe gives approximate M-S without full evaluation
   - Only proceed to full eval for top 3 combinations

4. AGGRESSIVE HILL CLIMBING:
   - For each candidate polygon, perform 5 rounds of refinement (not 3)
   - For each edge, try shifts: ±5, ±10, ±20, ±40, ±80 units (larger jumps)
   - Use grid-based scoring for fast evaluation
   - Keep best shift per edge

5. MULTI-PHASE RESTARTS:
   - Run 25 restarts (not 15-20)
   - Phase 1 (first 10 restarts): pure corridor expansion
   - Phase 2 (next 10 restarts): corridor + local mutation (swap vertices)
   - Phase 3 (final 5 restarts): aggressive expansion with large shifts

6. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords, no self-intersection)
   - Ensure perimeter <= 400,000
   - All coordinates in [0,100000]

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get exact score
- probe_corridor_combinations: Probe multiple corridor combinations cheaply
- finish: Submit when you have working solution

KEY DIFFERENCE from seed: 8-direction expansion, lenient stop criteria, combination probing, larger hill climbing shifts, phased restarts with mutations.
