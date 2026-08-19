You are optimizing a 29x29 +/-1 matrix to maximize |det(H)| for Hadamard optimization.
Key facts: n=29 == 3 mod 4, use Paley construction with quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.
H[i][j] = 1 if (i-j) mod 29 in residues, else -1.
Search Strategy:
1) Call analyze_paley_params once at start.
2) Build Paley base matrix correctly.
3) Apply MULTIPLE mutation strategies in parallel:
   - A: Simulated Annealing, T=3.0, cool=0.997, 25000 iterations per seed
   - B: Greedy hill-climbing (try all neighbors, accept only improvements)
   - C: Random perturbations (flip 3-8 positions, accept if better)
4) CRITICAL: DO NOT undo flips on rejection - explore all moves
5) Use numpy.linalg.det for ALL determinants (fast)
6) Try 5-8 different seeds per evaluation
7) Run each strategy for 10k-20k iterations, pick BEST result
8) Call probe_solution BEFORE evaluate_solution
9) Total runtime < 180 seconds per evaluation
10) Seed program has bug undoing rejected moves - fix it
Call edit_solution with complete working code implementing at least 3 strategies.
Call evaluate_solution once per evaluation. Always probe first.
