You are optimizing a 29x29 ±1 matrix to maximize |det(H)|.
n=29 ≡ 3 mod 4, so use Paley construction with quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

Build the Paley matrix where H[i][j] = 1 if (i-j) mod 29 in residues, else -1.

Then run simulated annealing hill climbing from this base. Use ONLY numpy.linalg.det for speed.

STRATEGY PER EVALUATION:
1. Build 6 different Paley base matrices using 6 different random seeds for the construction phase
2. From each base, run independent hill climbing with 15,000 iterations, T=3.0, cool_rate=0.997
3. Among all 6 results, pick the best determinant
4. Also try: perturb the best base matrix with 100 random ±1 flips, then hill climb 5,000 more iterations

Total operations: ~100k flips with numpy det = ~100 seconds, well under 350s budget.

You have 350 seconds per evaluate_solution call. NEVER timeout - keep total < 180s.

Always call probe_solution on different variants BEFORE evaluate_solution. Probe is cheap (~10s) and you have 30 probe budget.

Use edit_solution to replace EVOLVE-BLOCK with complete working code. Call evaluate_solution once per full evaluation attempt.

DO NOT use Bareiss during search. DO NOT exceed 180s runtime. DO NOT use more than 6 starting seeds.
