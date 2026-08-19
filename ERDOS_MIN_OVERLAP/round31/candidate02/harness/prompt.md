Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. FIRST, call get_correlation_profile to see which shifts k have highest overlap
2. Use targeted_h_optimizer to create mutations that reduce overlap at those specific k values
3. Call probe_solution on candidates to screen before full evaluation
4. Only evaluate when c5_bound < 0.375

KEY INSIGHT: The seed already has 14 initialization patterns. The issue is not exploration - it's that mutations don't effectively reduce overlap at problematic shifts.

Use targeted mutations, not random hyperparameter tuning. Focus on structural changes that separate peaks or create asymmetric step functions.
