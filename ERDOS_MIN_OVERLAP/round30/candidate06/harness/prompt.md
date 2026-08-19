Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

PHASE 1: DIVERSE INITIALIZATION
- Use search_patterns to generate 5-10 diverse initial step functions
- Screen with probe_solution (cheap, ~10s per candidate)
- Evaluate top 2-3 candidates with c5_bound < 0.375 using evaluate_solution

PHASE 2: ITERATIVE REFINEMENT (if Phase 1 yields no improvement)
- If best combined_score <= 1.0, use explore_neighbors to make targeted edits
- Start from the best pattern candidate, not the seed
- Use small, focused changes: adjust peak positions, split/merge intervals, shift thresholds
- Screen each variant with probe_solution before full evaluation
- Continue refining until either improvement or budget exhaustion

KEY INSIGHT: Both diverse initialization AND iterative refinement are needed.
Don't rely on hyperparameter tuning alone - the solver must explore the solution space systematically.

RULES:
- NEVER call evaluate_solution on c5_bound > 0.375 (wastes budget)
- Use probe_solution to screen all candidates before full evaluation
- If stuck, try explore_neighbors with different edit strategies
- Track best c5_bound across all attempts
