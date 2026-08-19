You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL INSIGHT: The problem is about finding compact clusters of mackerels while avoiding sardines.
The seed program's approach is too slow and misses optimal cluster patterns.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. INPUT ANALYSIS (use analyze_mackerel_clusters tool):
   - Parse fish positions from input
   - Group mackerels by proximity (within 2000 units)
   - Compute cluster density: mackerels_per_unit_area
   - Identify top 10 clusters by pure mackerel count
   - For each cluster, estimate minimum enclosing rectangle (MER)
   - Check if MER contains few sardines
   - Score clusters by (mackerels_in_MER - sardines_in_MER)

2. CLUSTER-BASED POLYGON CONSTRUCTION:
   - Start with highest-scoring cluster
   - Build MER around cluster mackerels
   - Expand MER slightly if it captures more mackerels with minimal sardine penalty
   - Ensure perimeter <= 400,000 and vertices <= 1000

3. COMBINE MULTIPLE CLUSTERS (if beneficial):
   - If two clusters are close enough, combine their MERs
   - Use union of rectangles (may need 8+ vertices)
   - Check if combined score improves

4. LOCAL OPTIMIZATION:
   - For each polygon edge, try small shifts (±1, ±2, ±5 units)
   - Keep shift that improves score without adding sardines
   - Limit to 2 refinement rounds

5. VALIDATION:
   - Output valid polygon (4-1000 vertices, integer coords, no self-intersection)
   - Ensure perimeter <= 400,000

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementing cluster-based optimization
- evaluate_solution: Run C++ program, get score
- probe_solution: Use with analyze_mackerel_clusters output to quickly test variations
- finish: Submit when you have encoded a working cluster-based optimizer

KEY DIFFERENCE from seed: Focus on compact mackerel clusters, not corridor expansion.
Use density analysis to find high-value regions and build minimal-perimeter polygons around them.
