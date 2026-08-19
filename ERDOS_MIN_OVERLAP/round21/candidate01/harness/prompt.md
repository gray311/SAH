Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).

STRATEGY - Use SMALL INTERVALS (N=200-400) for fast exploration, then refine with more intervals:

1. CALL generate_fast_candidates(temperature=0.7) to get 12 candidates with N=400 intervals.

2. EXAMINE all 12 candidates: check integral (~1.0) and c5_bound (precomputed analytical score).

3. CALL evaluate_solution on ALL candidates with c5_bound < 0.375.

4. If best score > seed, CALL generate_refine_candidates to get 3 refined candidates with N=800 intervals.

5. CALL evaluate_solution on the best refined candidate (c5_bound < 0.37).

6. Key insight: Fast candidates (N=400) are 4x cheaper - screen many, then refine promising ones.

7. Budget: Use 8-12 fast evals, 2-4 refined evals max.

Tools available: generate_fast_candidates (N=400), evaluate_solution (full, slow), probe_solution (approximate).
