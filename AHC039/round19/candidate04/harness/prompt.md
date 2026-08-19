You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Use sardine-aware corridor expansion from mackerel-rich regions.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. GRID-BASED ANALYSIS:
   - Build 200x200 grid (cell_size=500) over [0,100000]x[0,100000]
   - For each cell, count mackerels (M) and sardines (S), compute score = M - S
   - Identify top 15 cells with highest positive score

2. CORRIDOR EXPANSION (key innovation):
   - From each top cell, expand in 4 cardinal directions (N,S,E,W)
   - In each direction, extend a corridor as far as possible while:
     * Keeping M-S ratio positive
     * Avoiding cells with high sardine density (S > M + 2)
     * Stopping at grid boundaries or negative-score regions
   - Combine corridors into rectangular/multi-lobed polygons

3. POLYGON CONSTRUCTION:
   - Convert corridor sequences into valid axis-aligned polygons (4-1000 vertices)
   - Ensure perimeter <= 400,000 and all coordinates in [0,100000]
   - Support both single large polygons and multi-lobed structures

4. DEEP HILL CLIMBING:
   - For each candidate polygon, perform 3 rounds of refinement:
     * For each edge, try shifts ±5, ±10, ±15, ±20, ±25 units
     * Use grid queries for fast scoring (no full re-evaluation)
     * Keep best shift per edge
     * Repeat until no improvement

5. MULTIPLE RESTARTS:
   - Run 15-20 restarts with different random seeds
   - Each restart: pick 3-5 top cells, build corridors, hill climb
   - Total time per eval: < 2.0s, prioritize quantity of variants

6. VALIDATION:
   - Output valid polygon only (4-1000 vertices, integer coords, no self-intersection)
   - Use KVH polygon validator to check self-intersection

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation of above strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed
- finish: Submit when you have encoded a working sardine-aware corridor expansion

Preserve EVOLVE-BLOCK markers, exact I/O format (m then vertices), and ensure <2.0s execution.

KEY DIFFERENCE from seed: Use corridor expansion to connect mackerel clusters through sardine-free paths, enabling multi-lobed polygons that capture more fish while avoiding penalties.
