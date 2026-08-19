You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Cluster-based dense region targeting with multi-shape exploration.

SEARCH METHOD:

1. CLUSTER DETECTION:
   - Read all fish coordinates from input
   - Find regions with high mackerel density (>2 fish within 2000×2000 window)
   - Identify local maxima of (mackerels - sardines) in sliding 5000×5000 windows

2. SHAPE CONSTRUCTION (try multiple):
   - Square/rectangle around each cluster center
   - Diamond (rotated square) approximated with 8 vertices
   - Multi-cluster union: bounding box of multiple nearby clusters

3. SIZE PARAMETER SEARCH:
   - For each shape, try 5 different sizes: side_length × [10000, 15000, 20000, 25000, 30000]
   - Use rectangle sweep: slide window across cluster region to find best position

4. LOCAL REFINEMENT:
   - For promising candidates, try edge shifts of ±50, ±100, ±150 units
   - Test if expanding in one direction improves score

5. MULTI-SHAPE SELECTION:
   - Generate 8-12 diverse polygons using different shape templates and cluster combinations
   - Output the one with highest score

6. VALIDATION:
   - Ensure 4 ≤ vertices ≤ 1000, perimeter ≤ 400000, coordinates in [0,100000]
   - No self-intersection (axis-aligned polygons rarely self-intersect if built correctly)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing cluster-based approach
- evaluate_solution: Run C++ program, get score (mackerels-sardines+1)
- probe_solution: Not needed - direct evaluation required
- finish: Submit when you have 8+ shape variations and size search

KEY DIFFERENCE from seed: Use actual cluster detection and multi-shape construction instead of coarse grid corridors.
