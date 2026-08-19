You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

CRITICAL: The seed uses Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28} and simulated annealing with multiple restarts. The best score so far is 0.531724.

SEARCH STRATEGY: Focus on PARAMETER EXPLORATION of the existing Paley+SA approach, not new constructions.

PHASE 1 - Parameter Grid Search:
  - Vary: iterations (20k-40k), initial_temp (2.0-8.0), cool_rate (0.995-0.999), num_seeds (3-6)
  - Use quick_local_search tool to test 5-8 parameter combinations cheaply
  - Pick top 2 by probe score
  - Run FULL evaluation on best one

PHASE 2 - Targeted Escapes:
  - From Phase 1 best, try: (a) flip checkerboard pattern, (b) flip random 30% of entries, (c) flip positions where |i-j| in [5,10]
  - Each escape: 15k iterations, temp=5.0, cool_rate=0.992

PHASE 3 - Hybrid Approaches:
  - Take Phase 2 best, run 2 more SA restarts with: T=10.0 cool=0.999 (5k iters) then T=1.0 cool=0.998 (20k iters)

RULES:
  - Use numpy.linalg.det for ALL hill climbing (NEVER Bareiss during search)
  - Always call quick_local_search BEFORE evaluate_solution
  - Keep total runtime < 300s
  - Use all 20 evals if needed for thorough exploration

Start with Phase 1: implement parameter grid search with 8 variants.
