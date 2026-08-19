You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER-BASED APPROACH (fast, focused):
   - Parse fish coordinates, group mackerels that are close together (within 2000 units)
   - For each cluster, try building minimal enclosing rectangles (4-8 vertices)
   - Score each rectangle using exact evaluation
 
2. LOCAL SEARCH (key innovation):
   - Start with valid polygon (e.g., small rectangle capturing 1-2 mackerels)
   - For 8-10 iterations: try expanding edges outward by 50-500 units in 4 directions
   - Try shrinking edges inward by 10-100 units
   - Accept change if it improves score (simple greedy, no lookahead)
 
3. PERIMETER CONSTRAINT HANDLING:
   - Track current perimeter during expansion
   - Only accept moves that keep perimeter <= 400,000
   - If stuck, reset to smaller polygon and retry with different seed
 
4. MULTIPLE SEEDS:
   - Generate 8-12 candidate polygons from different mackerel pairs/points
   - Each seed: pick 2 random mackerels, build minimal rectangle between them
   - Run local search from each
 
5. VALIDATION:
   - Ensure 4-1000 vertices, integer coords in [0,100000], no self-intersection
   - Use simple point-in-rectangle and edge-intersection checks
   - Output best valid polygon
 
6. PERFORMANCE:
   - Total time < 2.0s per evaluation
   - Focus on speed: minimal data structures, avoid grid/KD-trees, simple arrays
   - Early termination if no improvement after 5 iterations
