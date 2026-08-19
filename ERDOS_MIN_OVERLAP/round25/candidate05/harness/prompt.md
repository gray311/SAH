Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL INSIGHT: The seed code has 15 hand-crafted mathematical initialization PATTERNS.
These are analytical constructions (Golomb ruler, bipartite, tri-modal) that may already be near-optimal.
Training with SGD (59000 steps) often DEGRADES these patterns.

STRATEGY:
1. FIRST and MOST IMPORTANT: Call generate_ready_candidates - this uses the seed's _get_best_initialization
   with patterns 12 (Golomb), 14 (Tri-modal), and 5 (Bipartite), computes c5_bound via FFT (no training!)
   This is ANALYTICAL - just FFT, no optimization needed.
2. Evaluate candidates with c5_bound < 0.375 using evaluate_solution
3. If no improvement, THEN try hyperparameter tuning with SMALL num_steps (5000-20000)
4. Use probe_solution to screen
5. Vary num_intervals (400, 800, 1600) for resolution

KEY: The seed patterns are mathematical constructions. TEST THEM FIRST without training!
