Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY: 
1. CALL validate_patterns FIRST to check if proposed patterns are structurally valid (h in [0,1], integral=1)
2. If validation passes, try TRAINING with: num_restarts=1, num_steps=30000 (fast test)
3. Use probe_solution to check c5_bound < 0.375 before full eval
4. For pattern construction: Golomb ruler marks at [0.0, 0.4, 0.8, 1.2, 1.6], Bipartite at x=0.5, Tri-modal peaks at [0.4, 1.0, 1.6]
5. EVALUATE ONLY when combined_score > 0.999
6. Key insight: Start with SIMPLE patterns, not complex training. The optimizer may overfit.
