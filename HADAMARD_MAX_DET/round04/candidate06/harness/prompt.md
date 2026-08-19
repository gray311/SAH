You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

MATHEMATICAL FACT: The Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28} produces a near-optimal Hadamard-like matrix. DO NOT try random matrices, perturbations, or alternative constructions - they cannot exceed the Paley optimum.

YOUR TASK: Take the Paley construction, then run EXTENSIVE simulated annealing hill climbing on it.

STRATEGY (EXACTLY):
1. Build Paley matrix from residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
2. Run simulated annealing: 80,000 iterations per seed with 3-stage cooling:
   - Stage 1: 20k iters, temp=15.0, cool=0.9985
   - Stage 2: 30k iters, temp=5.0, cool=0.997
   - Stage 3: 30k iters, temp=2.0, cool=0.999
3. Run with 5 seeds: [42, 123, 456, 789, 10000]
4. Use numpy.linalg.det for ALL determinant calculations (NEVER Bareiss during search)
5. Pick the best result across all 5 seeds.

TIME BUDGET: 80k iters × 0.001s ≈ 80 seconds per evaluation. Well under 350s.

TOOLS:
- edit_solution: Provide complete working code with Paley+80k iteration SA
- evaluate_solution: Call once on your best result
- probe_solution: Not needed - you have enough budget for one good search

KEY: Run MORE iterations on the CORRECT construction, not new constructions.
