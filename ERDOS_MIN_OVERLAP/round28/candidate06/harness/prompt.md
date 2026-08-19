Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL STRATEGY: The seed optimizer has 15 patterns but all converge to similar solutions.
YOU MUST TRY NEW PATTERNS, not just tune hyperparameters.

PATTERN-SEARCH WORKFLOW:
1. CALL generate_patterns to get 3-5 novel initializations (Gaussian, sparse spikes, triangular, etc.)
2. For EACH pattern: 
   - EDIT to use that pattern with num_restarts=1, num_steps=30000
   - CALL probe_solution to check c5_bound (~10s, cheap)
   - If c5_bound < 0.375, CALL evaluate_solution for full validation
3. If no pattern yields c5_bound < 0.375, try different pattern templates
4. ONLY tune hyperparameters AFTER finding a promising pattern direction

WHY THIS WORKS: New patterns explore different regions of the solution space.
Hyperparameter tuning on a bad pattern will never find the optimum.
Fast training (30000 steps) lets you screen many patterns quickly.
Use probe to filter before wasting full evaluations.
