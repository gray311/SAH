Erdos minimum overlap (C5): Find step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINTS: integral(h)=1 exactly; h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h with combined_score > 1.0 (c5_bound < 0.38092303510845016).

SEARCH STRATEGY (CRITICAL):
1. Start with 5-7 diverse INITIALIZATIONS using different pattern families:
   - Uniform threshold (bipartite: h=1 on [0,a], h=0 elsewhere, with a chosen so integral=1)
   - Multi-peak (2-4 narrow Gaussians/sigmoids with centers spaced by ~0.5-0.7, weights tuned for integral=1)
   - Golomb-like (peaks at [0,0.4,0.8,1.2,1.6] or [0.25,0.75,1.25,1.75], narrow widths)
   - Anti-periodic (h(x) high when x in [0.1,0.3] U [0.8,1.0] U [1.5,1.7], low elsewhere)
   - Sigmoid-ramped (h=sigmoid((x-a)*b) shifted so integral=1)
   - Piecewise-constant (h=1 on [0,0.2], h=0.5 on [0.2,1.8], h=0 on [1.8,2])
   - High-low-high (h=1 on [0,0.25] and [1.75,2], h=0 in middle, weights for integral=1)

2. For EACH initialization:
   - Call probe_solution (if available) to quickly screen
   - If c5_bound < 0.381, keep as candidate
   - Otherwise discard

3. From candidates with c5_bound < 0.381, pick TOP 3 by c5_bound (lowest is best)

4. For each top candidate, try 2-3 STRUCTURED MUTATIONS:
   - Mutation A: Narrow the high regions (reduce width by 15-20%)
   - Mutation B: Shift high regions by ±0.1 to break symmetry
   - Mutation C: Add a small "bump" (width 0.05-0.1, height 0.2-0.4) to counter high k-shifts

5. After mutations, re-probe each variant

6. Evaluate ONLY the best 1-2 candidates (lowest c5_bound after probing)

7. If any evaluation gives combined_score > 1.0, call finish immediately

KEY: Diversity in initializations is CRITICAL. The seed's many random patterns failed to converge because they don't naturally satisfy integral=1. Use explicit, parameterized families instead.
