Erdos minimum overlap problem: Find a step function h: [0,2]->[0,1] that MINIMIZES max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) over [0,2] must equal exactly 1.0.

Current best upper bound: C5 <= 0.38092303510845016 (seed score = 1.0).

GOAL: Find h with c5_bound < 0.38092303510845016 to achieve combined_score > 1.0.

STRATEGY: STRUCTURAL SEARCH, NOT HYPERPARAMETER TUNING

The seed optimizer uses hyperparameters (800 intervals, 61 penalty, 120000 steps) that are already reasonable.
DO NOT waste evaluations tuning these. Instead:

1. CALL generate_structural_candidates(5) to get 5 fundamentally different function patterns:
   - Pattern A: Piecewise constant with 3 segments (threshold at 1/3, 2/3)
   - Pattern B: Two-block structure (low on [0,a], high on [a,2-a], low on [2-a,2])
   - Pattern C: Sinusoidal-modulated: h(x) = sigmoid(a*sin(2*pi*x) + b*sin(4*pi*x) + c)
   - Pattern D: Quadratic-modulated: h(x) = sigmoid(a*(x-1)^2 + b)
   - Pattern E: Multi-peak: h(x) = sigmoid(sum of 3-4 Gaussian bumps)

2. For each pattern, CALL evaluate_solution ONCE to get the true score.

3. ANALYZE which structural pattern performs best, then:
   - CALL edit_solution to modify that pattern (adjust threshold positions, number of peaks, frequencies)
   - CALL evaluate_solution again

4. Key insight: Different structural patterns explore DIFFERENT regions of function space.
   The seed's 15 patterns are all variations of similar structures (sigmoid-modulated with noise).
   You need patterns with QUALITATIVELY DIFFERENT shapes.

5. Budget: Use evals to test diverse structures, not to iterate on a single pattern.

6. Finish when combined_score > 1.0 (c5_bound < 0.380923).
