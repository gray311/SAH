You are solving the Erdos minimum overlap problem: find a step function h: [0,2] -> [0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k)) dx.

Current best bound: C5 <= 0.38092303510845016 (combined_score = 1.0)
Goal: Find h with combined_score > 1.0 (c5_bound < 0.380923)

KEY INSIGHT: The optimal h likely has ASYMMETRIC BIMODAL structure with peaks at different locations to minimize overlap between h and h(x+k).

SEARCH STRATEGY (use all 30 evals):
Phase 1 - Generate diverse initializations:
  - Call generate_variants() to get 4-8 diverse candidate latent vectors
  - These include asymmetric bimodal, periodic, and multi-peak patterns
  - Convert each to h = sigmoid(latent), verify integral ≈ 1

Phase 2 - Rapid screening:
  - For each candidate, call probe_solution (fast, ~10s) to check:
    * Does integral(h) ≈ 1? (penalty should be < 100)
    * What's the approximate c5_bound?
  - Rank by: lowest c5_bound among those passing constraint check

Phase 3 - Full evaluation:
  - Call evaluate_solution on top 2-3 candidates that passed probe
  - Track best combined_score

Phase 4 - Refinement (if budget allows):
  - If a candidate shows promise (combined_score ~ 1.01-1.02), EDIT the EVOLVE-BLOCK
    to use THAT specific initialization pattern
  - Then run optimization from there with careful hyperparameter tuning

DO NOT just tune hyperparameters of the seed's existing initialization.
Generate NEW initializations first, then refine.

Success means combined_score > 1.0 (c5_bound < 0.380923)
