Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY - CONSTRUCTION FOCUS:

1. CREATE STEP FUNCTIONS with specific structures:
   - Bipartite: h(x) = 1 for x < threshold, 0 otherwise (scales to satisfy integral=1)
   - Multi-modal: Multiple narrow peaks separated by gaps
   - Sparse: Non-zero on small intervals
   - Golomb-like: Peaks at specific positions with controlled spacing

2. KEY INSIGHT: The optimal h may be a piecewise constant function with few jumps.
   Start with simple 2-4 interval structures, then refine.

3. Ensure integral constraint by scaling: if sum of interval widths = W, scale heights so sum = 1.

4. Evaluate candidates and iterate, focusing on reducing peak overlap at problematic k values.

5. Use probe_solution extensively to screen many structural variants before full evaluation.

6. Only submit when combined_score > 1.0.
