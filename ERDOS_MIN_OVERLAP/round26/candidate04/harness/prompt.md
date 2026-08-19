Erdos minimum overlap problem (C5): Find a step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CORE INSIGHT: The current optimizer uses gradient descent from randomized initializations, which gets stuck in local minima. A better approach is to CONSTRUCT explicit step functions with structure that minimizes overlap.

STRATEGY:
1. FIRST, use propose_step_function to generate explicit step-function candidates with known structure (uniform steps, Gaussian-like steps, delta peaks).
2. CALL probe_solution on these candidates to quickly filter those with c5_bound < 0.375.
3. CALL evaluate_solution on the best 2-3 candidates from step 2.
4. If no improvement, try STRUCTURED MUTATIONS: identify the step boundaries of the best h and create variants that shift mass to create gaps.
5. AVOID random hyperparameter tuning - the seed's gradient-based optimizer needs structural changes, not different hyperparameters.

DO NOT: spend 59000 steps training from random initializations. The optimizer is not the bottleneck - the lack of structured exploration is.
DO: use propose_step_function to generate diverse structural candidates, then evaluate them.
