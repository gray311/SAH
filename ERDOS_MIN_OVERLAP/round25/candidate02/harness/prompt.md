Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL WORKFLOW (MUST FOLLOW IN ORDER):

1. FIRST: Call generate_analytical_candidates to get 5-8 integral-constrained
   step functions with precomputed c5_bound scores. These are EXACT solutions,
   not SGD outputs.

2. FILTER: Keep ONLY candidates with c5_bound < 0.380 (about 3-4 should pass).
   Call evaluate_solution on EACH kept candidate.

3. If ANY candidate has combined_score > 1.0, CALL finish immediately.

4. If NO improvement after 2: Go to step 5.

5. SECONDARY: If still stuck, try hyperparameter sweeps BUT ONLY with
   num_restarts=1 and num_steps=30000 (fast checks). Never let the solver
   "learn from scratch" - the analytical candidates are the gold standard.

6. KEY INSIGHT: The Golomb ruler patterns with 4-5 marks at ~0.4, 0.8, 1.2, 1.6
   spacing are structurally optimal. Bipartite and tri-modal are baselines.
   The SGD optimizer WILL NOT beat these if they start at seed quality.

7. EVALUATION: Full eval takes 59k steps. Use probe_solution only if you have
   no analytical candidates left. Never waste evals on SGD runs from bad seeds.

8. If all analytical candidates fail (c5_bound >= 0.380), THEN explore
   hyperparameter variations ONE AT A TIME with probe_solution first.
