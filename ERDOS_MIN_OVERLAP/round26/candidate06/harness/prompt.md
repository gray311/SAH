Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

SOLVER STRATEGY:
1. FIRST: Call generate_ready_candidates to get 3 analytical candidates with precomputed scores.
   These candidates are already integral-constrained and ready for full evaluation.
   If any has c5_bound < 0.37, CALL evaluate_solution on it immediately.

2. SECOND: If no improvement, EDIT the seed program's pattern definitions (patterns 5, 12, 14)
   to explore new structural variations. Try modifying mark positions, peak widths, or
   amplitude ratios. Make SMALL, SPECIFIC edits that change the pattern structure.

3. THIRD: Use probe_solution to screen edited variants (c5_bound < 0.375). Only call
   evaluate_solution on probes with c5_bound < 0.37.

4. FOURTH: If still stuck, vary ONE hyperparameter at a time (num_intervals, base_learning_rate,
   penalty_strength) and use probe_solution to screen. Evaluate only when probe shows
   c5_bound < 0.37.

5. KEY INSIGHT: Gradient-based optimization (SGD in seed) may be stuck in local minima.
   Structural edits to pattern definitions can escape these. Focus on:
   - Golomb ruler: Try different mark spacings (0.4->0.5, 0.8->0.75, etc.)
   - Tri-modal: Try different peak positions [0.35, 1.0, 1.65] or [0.4, 1.1, 1.6]
   - Bipartite: Try different split points [0.4, 0.6, 0.7]
   - Amplitude ratios: Try different ratios in pattern 5, 12, 14

6. EVALUATE ONLY when combined_score > 0.99999 (c5_bound < 0.3809). Full evaluation is expensive.
7. If 15 iterations without improvement, restart with completely new pattern edits.
