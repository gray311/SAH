Erdos C5 minimization: Find h: [0,2]->[0,1] with integral(h)=1 minimizing max_k integral h(x)(1-h(x+k))dx.

CURRENT BEST: c5_bound ≈ 0.381 (combined_score = 1.0). Goal: c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: Seed has 15 patterns but optimizer may not escape local optima. Need NEW initialization patterns, not hyperparameter tuning.

SEARCH STRATEGY:
1. Use generate_variants to create 5 new initialization patterns (Golomb-7, tri-modal, bipartite, multi-peak, Golomb-5-shifted)
2. For each variant: check integral constraint, then call probe_solution
3. Evaluate ANY candidate with probe c5_bound < 0.375
4. If no success after 5 variants, try: num_intervals=400 or penalty_strength=100
5. NEVER just tweak learning rate - these rarely help without new initializations
6. USE probe_solution for ALL screening - only 30 evals total
7. After evaluation, propose STRUCTURED edits (new pattern parameters, not hyperparameters)
