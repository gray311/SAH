Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016 (combined_score > 1.0 means new record).

SEED OPTIMIZER: Runs 59000 training steps per candidate using sigmoid-scaled latent vectors.

STRATEGY - Pattern-Based Search:

1. CALL generate_valid_simple to get 3 EXACTLY integral=1 step functions:
   - Bipartite: h=2 on [0.5,1.0)
   - Two-block: h=1 on [0,0.5) and [1,1.5)
   - Tri-step: h=2.5 on [0.4,0.8)

2. Check c5_bound < 0.38 (integral is 1.0 by construction)

3. CALL evaluate_solution ONLY if c5_bound < 0.38

4. If nothing passes, regenerate or use generate_ready_candidates(temperature=0.8)

Budget: 30 evals. Max 4-5 full evaluations.

Finish when combined_score > 1.0.
