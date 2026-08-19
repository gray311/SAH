You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

PROBLEM INSIGHT: The optimal polygon should tightly enclose mackerel clusters while excluding sardines. Since vertices must be axis-aligned, think in terms of rectangles, L-shapes, and U-shapes.

SEARCH STRATEGY:

1. FAST LOAD AND FILTER:
   - Read fish coordinates, separate into mackerels and sardines
   - Sort both by x-coordinate for fast spatial queries
   - Build hash set for O(1) point lookup

2. GRID-BASED DENSITY MAP (fine-grained):
   - Use 200x200 grid (500x500 cells, cell_size=500)
   - For each cell, count mackerels (M) and sardines (S)
   - Compute cell quality = M - S
   - Mark cells as good if M - S > 0, bad if S > M + 1

3. POLYGON TEMPLATE GENERATION (key innovation):
   - Template A: Single rectangle - find top good cell, try rectangles centered there with sizes [2x2, 4x4, 6x6, 8x8, 10x10, 15x15, 20x20, 25x25, 30x30, 50x50]
   - Template B: L-shape - find two adjacent good cells, form L around their bounding box with various arm lengths [2,4,6,8,10,15,20]
   - Template C: U-shape - find three cells in L, form U-shape around them
   - Template D: Multiple rectangles - connect 2-5 good cells with corridors

4. CORRIDOR CONNECTION (refined):
   - Between selected seed cells, create minimal corridors
   - Only include cells where M >= S (don't add extra sardines)
   - Keep corridor width = 1 unit where possible

5. POLYGON CONSTRUCTION AND VALIDATION:
   - Convert cell selections to axis-aligned polygon vertices
   - Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]
   - Validate no self-intersection (edges only meet at endpoints)
   - Use bounding box of cells plus corridor width to create polygon

6. LOCAL SEARCH (targeted):
   - For each polygon candidate, try edge shifts: +1, +2, +3, +4, +5, -1, -2, -3 units
   - Check if shift improves score (fast O(N) count)
   - Repeat 2-3 refinement passes
   - Keep best variant

7. MULTIPLE RESTARTS:
   - Run 20-25 restarts with different random seeds
   - Each restart: random seed selection, 1-2 polygon templates, hill climb
   - Output best polygon found

8. EVALUATION:
   - Use precise point-in-polygon test for all fish
   - Score = max(0, mackerels - sardines + 1)
