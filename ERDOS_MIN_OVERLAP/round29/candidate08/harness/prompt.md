Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
KEY INSIGHT: The optimizer needs mathematically-informed initializations, not just hyperparameter tuning.
STRATEGY:
1. FIRST, USE generate_c5_candidates to create diverse, integral-constrained initializations with known C5 constructions (Golomb rulers, bipartite, triangular, multi-peak).
2. CALL evaluate_solution directly on each candidate from generate_c5_candidates (no probe needed - these are high-quality initializations).
3. If combined_score <= 1.0, THEN refine hyperparameters to systematically tune num_intervals, learning_rate, and penalty_strength.
4. NEVER waste evals on random latents - always use structured, mathematically-informed patterns first.
5. Use coarse-to-fine refinement: start with num_intervals=200 for faster evaluation, then increase to 800 for final optimization.
6. Track c5_bound across all candidates and report the best.
