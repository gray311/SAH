Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

CRITICAL: Use generate_ready_candidates to get VALID, integral-constrained initializations.

Strategy:
1. CALL generate_ready_candidates ONCE at the start
2. EXAMINE the three candidates' integral and c5_bound estimates
3. CALL evaluate_solution ONLY on candidates where c5_bound < 0.375 AND integral ~ 1.0
4. If none pass, CALL generate_ready_candidates again with different seeds
5. Never waste evals on integral-violating candidates

Key: The seed optimizer trains for 59000 steps. Use cheap analytical screening to pick winners.
