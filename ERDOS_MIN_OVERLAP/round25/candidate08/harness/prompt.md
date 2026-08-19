Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL STRATEGY: The seed optimizer trains for 59000 steps via gradient descent, but this often gets stuck.
Instead of tuning hyperparameters, INSTANTIATE HAND-CRAFTED PATTERNS that minimize overlap analytically:

PATTERN 1 (Two-step): h(x) = 1 on [0,1), h(x) = 0 on [1,2] - uniform split
PATTERN 2 (Three-step): h(x) = 1 on [0,1/3) U [2/3,2], h(x) = 0 on [1/3,2/3] - concentrated mass
PATTERN 3 (Five-step Golomb): h = 1 on [0,0.4) U [0.6,0.8) U [1.0,1.2) U [1.4,1.6) U [1.8,2.0], h = 0 elsewhere
PATTERN 4 (Four-step): h = 1 on [0,0.5) U [0.5,1.0), h = 0 on [1.0,2.0] - half-half-one
PATTERN 5 (Symmetric three): h = 1 on [0,0.333) U [0.666,1.0) U [1.333,2.0], h = 0 in between

For each pattern:
1. CALL edit_solution to replace h with your step function (use manual h array assignment)
2. CALL probe_solution to verify integral=1 and c5_bound < 0.37
3. If c5_bound < 0.37, CALL evaluate_solution for final score

After testing 3-5 patterns, if no improvement, THEN try hyperparameter tuning (num_intervals=400/800/1600,
penalty_strength=40/80/120, num_steps=30000/59000/80000).

KEY: PATTERNS beat hyperparameter tuning. The FFT-based evaluation is analytical - good candidates
should be found in O(1) probes. Aim for c5_bound <= 0.36.
