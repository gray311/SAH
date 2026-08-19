Erdos C5: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (score = 1.0).

GOAL: Find h with c5_bound < 0.38092303510845016 (score > 1.0).

STRATEGY: Systematic hyperparameter tuning, not pattern analysis.

The seed is an optimizer class with hyperparameters:
  - num_intervals: 400-1600 range (default: 800)
  - penalty_strength: 80-150 range (default: 61)
  - base_learning_rate: 0.001-0.01 (default: 0.004)
  - num_steps: 40k-200k (default: 120k)
  - num_restarts: 1-10 (default: 3)

1. Use hyperparameter_tuner to get mutation suggestions.
2. Vary ONE parameter at a time.
3. Use probe_solution to screen before full eval.
4. Focus on penalty_strength=100,120 and num_intervals=600,1000.
5. Call at least one hyperparameter variation before concluding.
