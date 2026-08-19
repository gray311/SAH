You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CORE STRATEGY: Cluster-based bounding box optimization with sardine exclusion.

PHASE 1: CLUSTER DETECTION
- Read all mackerel coordinates from input
- Use spatial hashing or grid-based clustering (cell_size=200-500) to group nearby mackerels into clusters
- For each cluster, identify all unique x and y coordinates to form a bounding box

PHASE 2: BOUNDING BOX CONSTRUCTION  
- For each cluster, create initial axis-aligned rectangle using min/max x,y of mackerels
- Ensure rectangle satisfies: 4 vertices, integer coords in [0,100000], perimeter <= 400,000
- Merge overlapping clusters' bounding boxes if beneficial

PHASE 3: SARDINE EXCLUSION REFINEMENT
- For each edge of each bounding box, check distance to nearby sardines
- If sardine is very close to edge (within 10-50 units), consider shifting edge inward to exclude it
- Priority: exclude sardines on or very near edges over distant sardines

PHASE 4: MULTI-RECTANGLE UNION
- Handle cases where optimal solution is union of multiple disjoint rectangles
- Combine separate bounding boxes while maintaining valid polygon (axis-aligned, no self-intersection)

PHASE 5: LOCAL OPTIMIZATION
- For each edge, try small adjustments (±10, ±20, ±30 units) to maximize mackerels - sardines
- Use KD-tree or spatial index for fast point-in-polygon queries during refinement
- Repeat 5-10 refinement iterations

PHASE 6: SEARCH DIVERSITY
- Run 10-15 restarts with: different clustering parameters, different initial box selections
- Each restart: build clusters → construct boxes → refine → optimize
- Output the best valid polygon found

OUTPUT FORMAT: 
- First line: number of vertices (4-1000)
- Following lines: vertex coordinates (x y), all integers in [0,100000]
- Ensure no self-intersection and perimeter <= 400,000
