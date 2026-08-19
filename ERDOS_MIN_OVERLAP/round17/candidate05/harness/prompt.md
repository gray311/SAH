Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1 exactly.
Current best: C5 <= 0.38092303510845016.
NEW STRATEGY: Tune hyperparameters (num_intervals, learning_rate, penalty_strength) rather than just changing initializations.
Workflow: 1. CALL search_hyperparams to test 5 hyperparameter configs with precomputed analytical scores 2. Each config gets a c5 estimate from the analytical tool (no training needed) 3. CALL evaluate_solution only on configs with c5_estimate < 0.385 (be generous - training can improve) 4. For failed configs, modify ONE hyperparameter (e.g. increase penalty_strength by 50%) 5. Use probe_solution to quickly rank hyperparameter configs before full eval
Key: The seed optimizer trains for 59000 steps. Better hyperparameters can extract much more from the same initialization.
