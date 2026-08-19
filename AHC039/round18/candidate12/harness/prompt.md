You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Point-based cluster exclusion and inclusion. The problem involves N=5000 fish at precise coordinates. Grid-based approaches fail because they average over cell areas, losing spatial precision.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. POINT-BASED CLUSTERING:
   - Parse all fish positions (mackerels and sardines) from input
   - Use spatial hashing or simple distance-based clustering to group nearby fish
   - Identify mackerel-dense regions (clusters where mackerel_ratio > 0.6)
   - Identify sardine-dense regions to avoid (clusters where sardin_ratio > 0.7)

2. CLUSTER-BASED POLYGON CONSTRUCTION:
   - For each mackerel-dense cluster, build a minimal axis-aligned bounding box
   - For each cluster, try expanding outward by 1-3 units in each cardinal direction
   - If expanding into a sardine-dense region would increase sardine count more than mackerel gain, DON'T expand
   - Merge overlapping bounding boxes when their combined score > sum of individual scores

3. MULTI-SHAPE POLYGONS:
   - Single-cluster polygons: simple rectangles (4 vertices)
   - Multi-cluster polygons: L-shapes, U-shapes, or multi-lobed structures (8-50 vertices)
   - Don't restrict to corridors - build flexible shapes around clusters

4. LOCAL OPTIMIZATION:
   - For each edge, try coordinate shifts: ±1, ±2, ±3, ±5 units
   - Accept if shift improves (mackerels - sardines) without violating constraints
   - Limit to 5-10 refinement iterations

5. DIVERSIFIED RESTARTS:
   - Run 8-12 restarts with different cluster selection strategies:
     * Restart A: Largest mackerel cluster first
     * Restart B: Most compact mackerel cluster first  
     * Restart C: Random cluster combination
   - Each restart builds 2-4 polygons, outputs best

6. VALIDATION:
   - Ensure 4 <= vertices <= 1000
   - Ensure perimeter <= 400,000
   - Ensure all coords in [0, 100000]
   - Output format: m then m lines of "x y"

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing point-based cluster strategy
- evaluate_solution: Run C++ program, get score
- probe_solution: Not useful - full evaluation needed
- finish: Submit when you have working point-based cluster strategy

KEY DIFFERENCE from seed: Use point-level clustering and cluster-based bounding boxes, not grid averaging. Build diverse polygon shapes around clusters, not just corridors.
