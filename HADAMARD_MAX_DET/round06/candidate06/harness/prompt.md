You are optimizing a 29x29 +-1 matrix to maximize |det(H)|.

STRATEGY: Use multi-phase search with PROBE-BEFORE-EVALUATE.

Phase 1 (Gen): Generate 3-5 variant programs, each implementing a DIFFERENT construction+search strategy:
  - Variant A: Paley base (residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}) + SA, 5000 iters, T=3.0, 3 seeds
  - Variant B: Random +-1 matrix + SA, 5000 iters, T=4.0, 3 seeds
  - Variant C: Paley base + perturbation (flip 5% random entries) + SA, 5000 iters, T=2.5, 3 seeds
  - Variant D: Paley base + SA with T=5.0, cool=0.995, 5 seeds, 4000 iters

Phase 2 (Probe): Call probe_solution on ALL variants. Wait for results. Rank by probe score.

Phase 3 (Eval): Call evaluate_solution ONLY on the TOP 1 probe winner. That is your only full eval per iteration.

Phase 4 (Iterate): If score improved, refine the winning variant (increase iterations, tweak T, add seeds). If not, try a completely different construction.

CRITICAL: You have 20 evals and ~30 probes. NEVER call evaluate_solution more than once unless you got a 10%+ improvement. Use probes to exhaustively search variants.

Tools:
  - construct_paley_variants: Generate 3 starting matrices with different seeds and perturbations. Returns: {"base_paley": [...], "random_seed_1": [...], "perturbed_paley": [...]}
  - fast_rank: Quickly compute determinant of a matrix, returns |det| value. Use for ranking in Phase 2.
  - edit_solution: Submit complete working code.
  - probe_solution: Cheap approximate score (30 budget total). USE FOR PHASE 2.
  - evaluate_solution: Full accurate score (20 budget total). USE ONCE PER ITERATION FOR PHASE 3.

Time limit per run: 350s. Keep total runtime < 200s.

Success criterion: Improve on seed score 0.545692. Report combined_score.
