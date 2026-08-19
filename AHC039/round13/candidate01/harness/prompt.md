You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Cluster-based polygon construction using KD-tree for efficient scoring.

METHOD:

1. READER PHASE: Parse input, build KD-tree of all fish points (5000 mackerels + 5000 sardines).
   Fish are given as: N fish at lines 0..N-1 (mackerels), lines N..2N-1 (sardines).

2. CLUSTER IDENTIFICATION: Use the KD-tree to find 5-10 high-density fish clusters.
   For each candidate cluster, compute tight axis-aligned bounding box.

3. POLYGON GENERATION: For each cluster's bounding box, generate multiple polygon variants:
   - Original rectangle
   - Rectangle shifted by ±10, ±20, ±30 pixels (staying in bounds)
   - Rectangle with aspect ratio variations

4. PROBE SCREENING: For each candidate polygon, use probe_solution (if available) OR
   compute a quick bounding-box approximation: score ≈ count_fish_in_rect(bounds).
   Keep only candidates with probe score > 1.5.

5. FINE TUNING: For promising candidates, perform vertex-level mutations:
   - Try shifting each vertex by ±5, ±10, ±15
   - Keep mutations that increase mackerels or decrease sardines
   - Iterate up to 3 refinement rounds

6. MULTIPLE RESTARTS: Run 25 restarts with different random seeds.
   Each restart: pick 3-5 random seed points from KD-tree, find local cluster, build polygon.

7. VALIDATION: Ensure polygon has 4-1000 vertices, perimeter ≤ 400,000, integer coordinates.
   Output format: first line = vertex count, then each vertex as "x y".

TIME BUDGET: Complete all work in < 2.0 seconds. Prioritize probe screening to avoid costly evaluations.

KEY DIFFERENCE from prior attempts: Use KD-tree for O(log N) fish queries, build polygons around actual fish clusters, use cheap probing to filter candidates before full evaluation.
