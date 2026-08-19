You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Cluster-based rectangular construction with strategic inter-cluster connections.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. CLUSTER DETECTION:
   - Read all mackerel coordinates
   - Use DBSCAN-like clustering with radius=8000 to group nearby mackerels
   - For each cluster, compute its bounding box

2. RECTANGULAR CONSTRUCTION:
   - For each cluster, create a minimal axis-aligned rectangle covering it
   - Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
   - Score = mackerels_in - sardines_in + 1
   - Filter: only keep rectangles with positive score

3. INTER-CLUSTER CONNECTIONS:
   - Sort remaining rectangles by score descending
   - Try connecting adjacent rectangles (sharing edge or close proximity)
   - When connecting, compute the combined polygon score
   - Allow connection even if connecting through low-score regions IF it enables capturing more fish
   - Maximum 5 rectangles per polygon

4. PERIMETER VALIDATION:
   - Ensure total perimeter <= 400,000
   - Each rectangle should have perimeter <= 300,000 to allow connections

5. MULTIPLE RESTARTS:
   - Run 20 restarts with different random seeds
   - Each restart: regenerate clusters with slight perturbations
   - Try different connection strategies (greedy, best-first)
   - Track best polygon across all restarts

6. VALIDATION:
   - Output valid polygon (4-1000 vertices, integer coords, no self-intersection)
   - Use a simple self-intersection check (no edge crossings)

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete C++ implementation of cluster-based rectangular construction
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - full evaluation needed
- finish: Submit when you have encoded a working cluster-based rectangular construction with 20 restarts

Preserve EVOLVE-BLOCK markers, exact I/O format (m then vertices), and ensure <2.0s execution.

KEY DIFFERENCE from seed: Use clustering to find natural mackerel groupings, build rectangles around them, and strategically connect high-value rectangles while accepting some sardine penalty for connection benefits.
