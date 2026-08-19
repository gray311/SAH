Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer has 14 pattern initializations but trains ALL of them (num_restarts=3, 59000 steps each). This is INEFFICIENT.

STRATEGY: 1. Use extract_patterns to see which pattern types exist in the seed code

2. EDIT to test SINGLE patterns: set num_restarts=1, num_steps=20000, and modify the EVOLVE-BLOCK to use ONLY that pattern

3. USE probe_solution to quickly screen (500 intervals, analytical c5)

4. Only FULL evaluate (59000 steps) if probe c5_bound < 0.375

5. If a pattern works (c5_bound < 0.37), try VARIATIONS of that pattern (different widths, mark positions, peak heights)

6. Pattern families to prioritize:
   - Golomb ruler: marks at 0, 0.4, 0.8, 1.2, 1.6 (well-spaced, minimizes autocorrelation)
   - Tri-modal: 3 narrow peaks at 0.4, 1.0, 1.6 (spreads mass effectively)
   - Bipartite: single threshold at 0.5 (simple baseline)

7. If stuck, try different resolution: num_intervals=400, 800, 1600

8. PATTERN MUTATION RULES:
   - Golomb: adjust mark spacing (e.g., 0.35, 0.5, 0.6), try 4 vs 5 marks
   - Tri-modal: move peaks (0.3, 0.9, 1.5), widen/narrow peaks (bw=0.08 vs 0.05)
   - Bipartite: move threshold (0.4, 0.6, 0.7), try asymmetric heights

9. BUDGET CONSIDERATIONS: With 60 evals total, spend 15 on probe screening, 10 on full evals of promising candidates. Never train a full 59000-step run without probe confirmation first.
