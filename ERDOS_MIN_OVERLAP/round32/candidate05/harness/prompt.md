Erdos C5 Problem: Find step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINTS: integral(h) = 1 exactly, h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.00001).
GOAL: Find h achieving combined_score > 1.0 (c5_bound < 0.380923).

SEARCH STRATEGY:

The seed program uses sophisticated patterns but may be stuck in a local optimum.
Try these diverse mutation types directly:

1. PEAK_SPACING: Create h with peaks at positions that are NOT multiples of small integers
   (avoid k=0.5, k=1.0 alignments). Try peaks at [0.3, 0.7, 1.3, 1.7] or [0.25, 0.75, 1.25, 1.75].

2. ASYMMETRIC_BIPARTITE: Use threshold at non-symmetric points like x=0.3 or x=0.4
   (current seed uses x=0.5, x=1.0 which may align badly with shifts).

3. MULTI_SCALE: Combine coarse structure with fine ripples. Example:
   Base: threshold at x=0.4; Fine: add small sine wave h(x) += 0.1*sin(10*pi*x)

4. GAP_STRATEGY: Create regions where h=0 (no overlap possible there)
   Pattern: h=1 on [0,0.3] U [1.4, 2.0], h=0 on (0.3, 1.4)
   Normalize to integral=1: h=1 on [0,0.333] U [1.333, 2.0]

5. FREQUENCY_SHIFTED: Use higher frequency base
   h(x) = sigmoid(3*pi*x - 1.5) shifted to have integral=1

For each edit:
- Ensure integral(h) = 1 exactly (adjust peak widths or values)
- Keep h in [0,1]
- Test with probe first if available

Use edit_solution to implement these patterns. Call evaluate_solution when you believe
you have a promising candidate.
