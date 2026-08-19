You are an expert mathematician and software developer. Task: Find a 29x29 ±1 matrix maximizing |det(H)|.

MATHEMATICAL FACT: n=29 ≡ 3 (mod 4), so true Hadamard matrices don't exist, but Paley construction gives near-optimal solutions.
Theoretical maximum is ~155.5, but achievable ~100-140.

SEARCH STRATEGY: The seed program's simulated annealing gets stuck in local optima. Use this approach:
1. CORRECT PALEY: Build from quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
2. MULTI-LEVEL REFINEMENT:
   - Phase 1: Run SA from Paley with 3 DIFFERENT cooling schedules (T=10,0.999; T=5,0.997; T=3,0.996)
   - Phase 2: Take BEST result, apply focused local search (random 100-point perturbations, then SA with T=100)
   - Phase 3: Try cross-matrix recombination (swap rows between top 3 candidates)
3. SEED DIVERSITY: Use 7 seeds total - 3 from Paley, 3 random matrices, 1 from Phase 2 refinement
4. FAST DET: ALWAYS use numpy.linalg.det for all iterations. NEVER use Bareiss during search.
5. BUDGET: ~200,000 total flips with numpy det (~25s) leaves time for refinement.

Tools:
- edit_solution: Provide FULL working code implementing the multi-phase strategy above
- evaluate_solution: Returns combined_score (higher=better). Budget=20. Best version auto-kept.
- probe_solution: Cheap ~10s approximate score. Use to test 2-3 cooling schedules BEFORE full eval.
- finish: End when no improvement after exhausting strategies.

CRITICAL: If your code uses Bareiss determinant during hill climbing, it will timeout. Use numpy only.
