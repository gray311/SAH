Erdos C5 Optimization: Minimize max_k integral h(x)(1-h(x+k))dx for h:[0,2]->[0,1] with integral(h)=1.

CURRENT BEST: c5 <= 0.38092303510845016 (combined_score = 1.0)
GOAL: Find h with c5_bound < 0.38092303510845016 (combined_score > 1.0)

STRATEGY: SYSTEMATIC PATTERN PERTURBATION

1. START WITH MODIFIED SEED PATTERNS - Don't generate new patterns from scratch. Instead,
   systematically perturb the seed program's 15 existing patterns:
   - Change Golomb marks positions (try [0.0, 0.4, 0.8, 1.6], [0.0, 0.5, 1.0, 1.5], etc.)
   - Vary bipartite thresholds (a = 0.4, 0.5, 0.6, 0.7)
   - Adjust peak widths and heights in multi-peak patterns
   - Experiment with triangular center positions

2. CALL analyze_pattern_effect to compute approximate c5_bound for each perturbation
   (uses FFT on 500 intervals - cheap, separate probe budget)

3. CALL evaluate_solution only on patterns with c5_bound < 0.378
   (allows some margin below seed: 0.3809)

4. If no improvement after 3-4 pattern variations, try hyperparameter tuning:
   - num_intervals: [400, 800, 1600]
   - penalty_strength: [40, 61, 100, 150]
   - base_learning_rate: [0.001, 0.004, 0.01]

5. Use analyze_pattern_effect to guide which perturbations to try next.
EVALUATE ONLY when c5_bound < 0.378 (combined_score > 1.006)
