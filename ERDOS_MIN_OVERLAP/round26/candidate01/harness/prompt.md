Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
CRITICAL INSIGHT: The seed optimizer uses gradient descent over 59,000 steps. This is TOO SLOW and gets STUCK in local minima.
STRATEGY: 1. Use pattern_evaluator to TEST READY-MADE PATTERNS ANALYTICALLY (no training). 2. Focus on discrete pattern constructions that distribute mass to minimize overlap. 3. Only use evaluate_solution on patterns with c5_bound < 0.378 (probe says "promising"). 4. Try varied pattern types: well-sparse marks, narrow multi-peaks, bipartite splits. 5. Avoid retraining - patterns that work analytically should work with full eval.
PATTERN CLASSES TO TRY: - Golomb ruler: marks at well-separated positions [0, 0.4, 0.8, 1.2, 1.6] - Tri-modal: 3 narrow peaks at [0.4, 1.0, 1.6] each with small bandwidth - Bipartite: h=1 on [0, a), h=0 on [a, 2] with integral normalization
WORKFLOW: CALL pattern_evaluator to get 3-5 candidate patterns with precomputed c5_bound. Pick those with c5_bound < 0.378. CALL evaluate_solution on top candidates. If none work, try different pattern classes.
