Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. FIRST, use correlation_analyzer to understand the current best solution structure
2. Identify which shifts k have the highest overlap integral
3. Use structure_inspired_mutations to create targeted improvements focusing on reducing overlap at those k values
4. Call probe_solution on candidates before full evaluation
5. Only evaluate when c5_bound < 0.375

KEY INSIGHT: Random patterns fail because they don't satisfy the integral constraint.
Use analysis-driven mutations instead of pattern-based approaches.
