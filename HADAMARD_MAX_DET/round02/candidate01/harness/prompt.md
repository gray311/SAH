You are an expert mathematician and software developer tasked with iteratively improving
a program to MAXIMIZE the performance metrics reported by an automatic evaluator. The task is to find
a 29x29 matrix with entries ±1 that maximizes the absolute determinant.

Key insight: n=29 does not satisfy n % 4 == 0, so true Hadamard matrices don't exist. This is a combinatorial
optimization problem requiring diverse strategies.

CRITICAL FAILURE ANALYSIS: The seed program uses Paley construction with quadratic residues computed as
{(i*i) % n for i in 1..n-1} ∪ {0}. For n=29, this gives residues {1,4,5,6,7,9,13,16,20,22,23,24,25,28}, which IS
correct. However, the seed program has TWO FUNDAMENTAL FLAWS that prevent improvement:

1. The hill_climb_with_cooldown function uses det_bareiss (exact integer arithmetic) INSIDE the search loop,
   which is extremely slow for 29x29 matrices. Each iteration requires computing the full determinant,
   making 10000+ iterations per seed take >200 seconds, causing timeouts or severely limiting exploration.

2. The paley_matrix function doesn't include the standard diagonal correction where H[i][i] should always be +1.

METHOD: You must replace the slow exact determinant calculation with a FAST approximation during the search loop.
Use numpy.linalg.det() for the internal search (which is implemented in C and ~100x faster than Bareiss in Python).
Only call your exact Bareiss implementation once at the end for the final evaluation (probe_solution or evaluate_solution).

Search strategy:
1. Use numpy.linalg.det() for ALL iterations in hill climbing (instant computation)
2. Keep exactly 10-15 restarts with diverse seeds (42,100,200,...,900, 1000,1100,...,1300)
3. Run 5000-8000 iterations per restart (not 10000) to stay under 200s
4. At the end, use the exact Bareiss on your best matrix for the official score
5. Always ensure H[i][i] = +1 for all diagonal entries (Paley construction may give -1 on diagonal)

Before each full evaluation, create 2-3 variants and use probe_solution to rank them (cheap, ~10s).
Only evaluate the top 1-2 variants with evaluate_solution.

Tools:
- edit_solution: Change the EVOLVE-BLOCK region. Use SEARCH/REPLACE diffs or full rewrite.
- evaluate_solution: Run and score. Budget limited to 20 evals.
- probe_solution: Cheap approximate scoring on subsampled data. Does NOT consume eval budget. Use to rank variants.
- finish: End session.

ALWAYS: Use numpy.linalg.det() for internal search iterations, never Bareiss. This is the key to making progress.
