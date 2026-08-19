You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

Use ONLY the Paley construction with quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.
For H[i][j]: diff = (i-j) mod 29, set H[i][j] = 1 if diff in residues else -1.

Then apply simulated annealing from this starting matrix:
- Run 100,000 flip iterations total
- Start with temperature T=5.0
- Cool at rate 0.997 per iteration
- At each step: flip one random element, compute determinant, accept if better OR with probability exp(delta/T)

Use numpy.linalg.det for ALL determinant calculations (never Bareiss during search).

Try 8 different random seeds for the flip sequence: [42, 123, 456, 789, 2024, 2025, 2026, 2027].
For each seed, run the full 100k iteration annealing from the Paley base.
Return the matrix with the highest determinant found.

Expected runtime: ~100k × 0.001s ≈ 100 seconds per seed × 8 seeds = 800 seconds total.
BUT you have 350 seconds per evaluation. SO YOU MUST RUN ONLY 4 SEEDS per evaluation.

Call edit_solution with complete working code implementing exactly this strategy.
Call evaluate_solution once per evaluation.

DO NOT implement multiple construction methods. DO NOT use Bareiss. DO NOT exceed 4 seeds.
