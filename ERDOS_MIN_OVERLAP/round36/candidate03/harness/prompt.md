Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. FIRST, generate valid step functions using generate_bipartite_step or generate_multimodal_step
   - Bipartite: single threshold at position t in [0,2], h(x) = 1 if x < t else 0
   - The threshold t must satisfy: t * 1 + (2-t) * 0 = 1, so t = 1.0
   - But we can have multiple thresholds: sum of (width_i * height_i) = 1

2. Use generate_bipartite_step to create a threshold function at t=1.0 (single peak)
   - This is mathematically guaranteed to satisfy integral(h) = 1
   - Then refine this solution

3. Identify high-overlap shifts using evaluate_solution
4. Create mutations to reduce overlap at those specific k values

5. Use probe_solution to screen candidates before full evaluation

6. Only evaluate when c5_bound < 0.375

KEY INSIGHT: Start with analytically valid step functions (bipartite, multimodal) rather than
trying to mutate complex neural network-like solutions. Simple geometric shapes often beat
complex patterns for this integral minimization problem.
