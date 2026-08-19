You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

STRATEGY: Use rectangle sweep-line optimization for efficient scoring.

APPROACH:
1. PARSE ALL FISH: Read mackerels and sardines from input
2. BUILD 2D GRID: Create 1000x1000 grid (cell_size=100) for fast counting
3. COUNT FISH PER CELL: O(N) pass to populate grid
4. BUILD PREFIX SUMS: O(1) rectangle score query via 2D prefix sums
5. SEARCH HIGH-VALUE RECTANGLES: Try sweeping over all possible rectangle boundaries (0 to 100000), use prefix sums for instant M-S score
6. VALIDATE: Check perimeter <= 400,000, vertices <= 1000, coords in [0,100000]
7. OUTPUT: Best valid polygon (rectangle or multi-rectangle)

KEY DIFFERENCE from seed: Use prefix sum 2D array for O(1) score queries enabling exhaustive boundary search within time limit. Seed only uses KD-tree and doesn't enumerate rectangles efficiently.
