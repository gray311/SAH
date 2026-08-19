You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Exploit axis-aligned rectangle union properties and use directional growth from high-density regions.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. X-Y COORDINATE BINNING:
   - Bin fish positions into a 400x400 grid (cell_size=250)
   - For each bin, compute score = mackerels - sardines
   - Identify top 8 bins with highest positive score

2. RECTANGLE PROLIFERATION:
   - For each top bin, grow rectangles in all axis-aligned combinations
   - Try: fixed size rectangles, growing rectangles, and unions of 2-3 adjacent rectangles
   - Use efficient bounding box expansion with early termination

3. DIRECTIONAL GROWTH (key innovation):
   - From high-scoring rectangles, attempt to extend in one direction only
   - This creates L-shaped or elongated structures that can capture clusters
   - Extension continues while marginal gain > 0 and perimeter < 400,000

4. STRAIGHT-LINE UNIONS:
   - Combine multiple collinear rectangles into a single shape
   - This reduces perimeter penalty while maintaining coverage
   - Valid only if rectangles share an edge (no overlap, just adjacency)

5. HILL CLIMBING:
   - For each candidate: try vertex shifts of ±10, ±20 units on all edges
   - Use efficient O(1) score lookup from coordinate bins for small movements
   - Repeat 2 rounds, keep best

6. RESTART STRATEGY:
   - 8 restarts with seeds from: top bins, bounding box corners, random offsets
   - Each restart explores: single rectangles, L-shapes, straight-line unions
   - Track best polygon across all restarts

7. VALIDATION:
   - Output valid polygon (4-1000 vertices, integer coords, no self-intersection)
   - Perimeter <= 400,000, coords in [0,100000]

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed
- finish: End when you have encoded a working optimizer

Preserve EVOLVE-BLOCK markers, exact I/O format (m then vertices), <2.0s execution.
KEY IMPROVEMENT: Coordinate binning + rectangle union strategies for efficient exploration.
