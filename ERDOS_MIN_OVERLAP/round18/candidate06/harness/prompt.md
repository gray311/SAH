Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

ROOT CAUSE: The seed program's multi-restart strategy already runs 15 diverse initializations and trains each for 59000 steps (3 restarts = ~177k total steps). The harness must NOT waste evals on retraining similar seeds.

STRATEGY: ONE-SHOT ANALYTICAL SCREENING WITH DIVERSE PATTERNS

1. CALL generate_ready_candidates ONCE with temperature=0.8 (more diverse than 0.5)
   - This returns 3 candidates with precomputed integral and c5_bound (analytical, no training)
   - Patterns: Golomb ruler, Bipartite, Tri-modal — all integral-normalized

2. FILTER: Keep ONLY candidates with:
   - integral within [0.95, 1.05] (tolerance for numerical error)
   - c5_bound < 0.365 (stricter than 0.37 to ensure margin over current best)

3. EVALUATE: CALL evaluate_solution on each kept candidate
   - Each full eval costs 1 from budget (30 total)
   - With 3 candidates and lenient filter, we use 3 evals max

4. DECISION:
   - If any combined_score > 1.0 (c5 < 0.3809), CALL finish immediately with summary
   - If none improve, CALL finish anyway (document that analytical screening found no better seeds)

KEY: The seed optimizer's training phase is computationally heavy but effective at local optimization.
Our job is purely to FIND BETTER INITIAL SEEDS analytically — no training needed.
Use the probe budget wisely: generate_ready_candidates is cheap (uses probe budget, not eval budget).
Only spend full evals on candidates with c5_bound < 0.365 to ensure a meaningful margin.
