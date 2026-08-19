Erdos C5 problem: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: combined_score > 1.0.

ROOT CAUSE: The seed optimizer's hyperparameter search is insufficient. The optimizer needs STRUCTURAL CHANGES to the step function h, not just hyperparameter tuning.

STRATEGY:
1. FIRST: Call mutate_h_structure to generate structurally different step functions (shift peaks, split intervals, merge regions).
2. Use probe_solution to screen candidates (cheap, ~10s per candidate).
3. Call evaluate_solution on top 2-3 candidates with c5_bound < 0.375.
4. ONLY if no improvement after 2 structural searches, THEN tune hyperparameters (num_intervals, learning_rate, penalty_strength).

KEY: Structural search (changing h's shape) is MORE important than hyperparameter tuning.
