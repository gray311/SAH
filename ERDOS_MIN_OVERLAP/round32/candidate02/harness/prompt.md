Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The optimal solution is likely a BIPARTITE STEP FUNCTION (two-level function that transitions from 1 to 0 at some threshold t).

STRATEGY:
1. Use bipartite_searcher to generate bipartite functions with different thresholds
2. For threshold t: h(x) = 1 if x < t, h(x) = 0 if x >= t
3. The integral constraint integral(h) = 1 means: t * 1 + (2-t) * 0 = t = 1, so t should be near 1.0
4. But we can perturb: try t in [0.8, 1.2] and let the optimizer fine-tune
5. Call probe_solution on candidates before full evaluation
6. Only evaluate when c5_bound < 0.375

WORKFLOW:
- Generate 5-10 bipartite candidates with thresholds in [0.7, 1.3]
- Probe all to screen for c5_bound < 0.382
- Evaluate the best 2-3
- If no improvement, try multi-modal patterns
