Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (c5_bound < 0.380923).

Strategy:

1. CALL generate_single_candidate to get ONE valid h(x) with integral=1.0

2. CALL probe_solution to get fast c5_approx (500 intervals)

3. If c5_approx < 0.38, CALL evaluate_solution for full score

4. If evaluate returns improvement, KEEP it and iterate:

   - Use edit_solution to try small mutations to the winner
   - Common mutations: shift peaks, adjust peak heights, merge adjacent intervals
   - Always check integral=1.0 after editing

5. If c5_approx >= 0.38, CALL generate_single_candidate again (different pattern)

6. Use hill-climbing: refine ONE good candidate before exploring new ones.

7. Total: 10-20 iterations with 2-3 evals each = 20-60 evals (we have 30).

Key: Quality over quantity. Find one good candidate and refine it.
