Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999945 (c5_bound < 0.380923).

CRITICAL INSIGHT: The seed optimizer uses gradient descent with sigmoid initialization.
This approach NEARLY always produces a candidate with c5_bound ~0.3809 (the seed).
GRADIENT DESCENT STALLS because the landscape is flat near the current solution.

NEW STRATEGY: IGNORE GRADIENT DESCENT. Instead, we will:

1. CALL generate_structured_patterns to get INITIALISATION that ARE NOT gradients
   of the current solution. These are analytical constructions from literature:
   - Golomb ruler: marks at 0, 1/5, 2/5, 3/5, 4/5 (spacing 1/5)
   - Bipartite: split [0,1] and [1,2] with different densities
   - Tri-modal: 3 peaks at 1/6, 1/2, 5/6
   - Sparse peaks: 2 narrow peaks at specific locations
   - Uniform flat: constant h(x) = 0.5 (integral = 1)

2. Analyze these patterns: check integral (~1.0) and c5_bound (precomputed)

3. CALL evaluate_solution on ALL candidates with c5_bound < 0.375

4. If none pass, try DIFFERENT pattern types (not new random seeds)

5. After each full eval, DO NOT EDIT the code to run gradient descent.
   Instead, generate a completely NEW pattern-based candidate.

Key: We are NOT improving the current solution. We are SEARCHING for a BETTER
starting point entirely. Each eval is a FULL re-run from scratch with a new pattern.
