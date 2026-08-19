Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999945 (c5_bound < 0.380923).

Strategy:

1. CALL generate_many_candidates to get 10+ diverse initializations

2. Analyze candidates: compute approximate c5_bound (use tool's precomputed value)

3. CALL evaluate_solution on candidates with c5_bound < 0.36 (generous threshold)

4. If no improvement, generate a new batch with different temperature

5. Never waste evals on integral-violating candidates

6. The seed optimizer uses 15 pattern variations - we need to explore MORE, not fewer.
7. Use 2-3 evals per iteration, and run 15-20 iterations to exhaust the 30 eval budget.

Key: Generate MANY diverse candidates, screen cheaply, evaluate the best.
