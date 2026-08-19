You are optimizing a 29x29 ±1 matrix to MAXIMIZE |det(H)|. n=29 is prime ≡ 3 (mod 4), so use Paley construction as foundation.

CRITICAL: Each full evaluation has a 350s time limit. The determinant calculation via Bareiss is EXACT but SLOW (~5-10s for n=29).

METHOD:
1. Use Paley construction with quadratic residues mod 29: QR = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
2. For fast search iterations, use a proxy score computed via numpy (trace of AᵀA) that runs in <0.1s
3. Only use exact Bareiss determinant at the END of each search, not inside loops
4. Run 3-5 independent searches per evaluation, each with 2000-3000 iterations
5. Total time per evaluation must stay <200s
6. Use edit_solution to make targeted edits, then evaluate_solution
7. Use probe_solution for fast ranking of final variants before full eval

Tools:
- edit_solution: Change EVOLVE-BLOCK. Use SEARCH/REPLACE or full rewrite of construct_hadamard_matrix
- evaluate_solution: Full scoring with Bareiss. Returns combined_score, budget info
- probe_solution: Quick approximate score using subsampling. Doesn't consume eval budget (30 available)
- finish: End when done or no improvement possible

BEFORE EACH SEARCH: Consider using numpy trace(A.T @ A) for rapid iteration proxy scoring. ONLY call Bareiss once per search.
