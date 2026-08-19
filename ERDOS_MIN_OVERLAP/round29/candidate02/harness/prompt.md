Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer (59000-step JAX training) ALREADY finds good solutions (combined_score=0.99997).
The harness's job is NOT to bypass the optimizer, but to IMPROVE ITS INITIALIZATIONS.

STRATEGY:

1. FIRST, CALL generate_optimizer_seeds to get 10 diverse latent-space initializations
   - Each is designed to seed the seed optimizer's training loop
   - Patterns: Golomb, Bipartite, Triangular, Multi-peak, Random-structured

2. RUN THE SEED OPTIMIZER on EACH seed (edit_solution to use that seed's latent, then evaluate)
   - The seed optimizer does 59000 gradient steps - it can refine bad starts into good solutions
   - Don't waste evals on precomputed patterns - let the optimizer do the work

3. If all 10 seeds produce combined_score <= 0.99997, THEN try hyperparameter variations:
   - num_intervals: 400, 1600, 3200
   - base_learning_rate: 0.001, 0.01
   - penalty_strength: 30, 100

4. NEVER skip the optimizer's training - the 59000 steps are where improvement happens

EVALUATE EACH SEED-INITIALIZED SOLUTION: The seed optimizer will take it from a bad start to the best it can find.
Pick the best result across all seeds.

Use generate_optimizer_seeds to get diverse, training-ready initializations.
