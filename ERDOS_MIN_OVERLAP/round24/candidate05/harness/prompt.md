ERFDS MINIMUM OVERLAP (C5) - FIND h: [0,2]->[0,1] MINIMIZING MAX_K INTEGRAL h(x)(1-h(x+k))dx.

HARD CONSTRAINTS:
- integral(h) = 1.0 exactly (within 1e-4 tolerance for FFT normalization)
- h(x) in [0,1] for all x

CURRENT BEST: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving combined_score > 1.0 (c5_bound < 0.38092303510845016).

KEY INSIGHT FROM SEED:
The seed's _get_best_initialization tries 15 pattern variations and returns the one with lowest c5_bound BEFORE ANY TRAINING.
This analytical pre-screening is PROVING EFFECTIVE - candidate k=7 achieved improvement by leveraging this.

FAILURES OF PREVIOUS HARNESSSES:
- 6/7 harnesses made NO PROGRESS (stuck at seed score).
- They failed because they over-relied on iterative hyperparameter tuning (gradual LR/penalty/interval changes)
- This is SLOW and often gets stuck in local optima
- The seed's 15 pattern search is BETTER: it explores diverse constructions analytically in one eval

NEW STRATEGY: EXTERNAL SEARCH VIA ppo_optimizer RESTARTS
The seed uses num_restarts=3 but the harness is SETTING num_restarts=1.
We need num_restarts >= 5 (ideally 10) to explore more pattern variations.
Higher num_restarts = more diverse initializations = better chance of finding good starting points.

SEARCH SPACE:
1. START WITH SEED NUM_INTERVALS=800, num_restarts=10, num_steps=59000, penalty_strength=60.0
2. Use probe_solution to check c5_bound BEFORE full eval
3. Only evaluate if probe shows c5_bound < 0.382
4. If no improvement after 3 attempts, VARY num_restarts (5, 10, 15, 20) and base_learning_rate
5. Try num_intervals in [400, 800, 1600] - but keep num_restarts HIGH throughout

CRITICAL: num_restarts MUST be 10+ to match the seed's 15-pattern diversity.
Lower restarts = fewer diverse initializations = worse exploration.
