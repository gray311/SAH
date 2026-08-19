Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
KEY INSIGHT: The seed optimizer already generates 15 diverse patterns via _get_best_initialization. We need to TUNE the training loop, not generate new patterns.
STRATEGY: 1. START with num_intervals=400 (faster evals, more iterations in budget) 2. INCREASE num_restarts to 5-7 to explore diverse initializations 3. Try base_learning_rate in [0.001, 0.003, 0.006, 0.01] for different convergence behaviors 4. Keep num_steps=59000 (full training) 5. After 2-3 successful runs, try num_intervals=600 or 800 for finer search 6. NEVER call search_patterns - use the seed's built-in pattern diversity
