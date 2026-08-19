Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
STRATEGY:
1. Use correlation_analyzer to find top 5 problematic shift values k (highest overlap)
2. Use mutation_generator to CREATE ACTUAL MUTATIONS that reduce overlap at those k values: - For each problematic k, try: (a) narrow the h peak, (b) shift h locally, (c) flatten h in the overlap region - ALWAYS preserve integral(h)=1 by adjusting values proportionally - h must stay in [0,1]
3. Generate 3-5 mutations using mutation_generator 4. Call probe_solution on each to screen (c5_bound < 0.375) 5. Evaluate best candidate(s) 6. If no improvement, repeat with different mutation strategies
KEY: The solver MUST actually edit h values based on correlation analysis. Use mutation_generator to generate real edits, not just notes.
