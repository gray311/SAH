Erdos minimum overlap (C5): Find h:[0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h)=1 exactly. h in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score=1.0).
GOAL: Find h with c5_bound < 0.38092303510845016 (combined_score > 1.0).

PRIMARY STRATEGY: Explore DIFFERENT initialization PATTERNS first (not hyperparameters).

INITIALIZATION PATTERNS (call generate_pattern_candidates once):
1. Golomb ruler: marks at [0.0, 0.4, 0.8, 1.2, 1.6]
2. Bipartite: high on [0,0.5), low on [0.5,2]
3. Tri-modal: 3 narrow peaks at [0.4, 1.0, 1.6]
4. Golomb variant: marks at [0.0, 0.45, 0.9, 1.35, 1.8]
5. Bipartite variant: split at a=0.6
6. Uniform baseline: h(x) ~ 0.5 everywhere
7. Two-bump: peaks at [0.3, 1.7]
8. Skewed bimodal: peaks at [0.2, 1.5]

WORKFLOW:
1. CALL generate_pattern_candidates ONCE to get 8 diverse initializations
2. Use probe_solution to screen all 8 (cheap, ~10s each)
3. Evaluate the 2-3 best with combined_score improvement using evaluate_solution
4. If no success, THEN vary ONE hyperparameter (num_intervals, learning_rate, penalty)

KEY INSIGHT: The seed's 15 patterns may all converge to similar local minima. 
Fresh pattern designs (Golomb, bipartite, tri-modal) may escape the seed's optimization basin.

BUDGET: 60 evaluations. Each training run (num_steps=59000) is expensive (~1 eval).
Use probe_solution heavily to filter bad candidates before full evaluation.
