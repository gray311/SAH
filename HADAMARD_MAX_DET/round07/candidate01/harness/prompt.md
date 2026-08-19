You are optimizing a 29x29 ±1 matrix to maximize |det(H)|.

CRITICAL INSIGHT: The seed uses Paley construction with SA tuning, but this traps you in a local optimum.
Your goal is to ESCAPE by trying DIFFERENT matrix construction strategies, not just tuning SA parameters.

STRATEGY: Run a "construction competition" where you try 3-5 DIFFERENT matrix generators in parallel:
1. Paley construction (as seed) - Quadratic residues mod 29
2. Random ±1 matrix with SA refinement
3. Low-discrepancy sequence based (Sobol/Halton) initialization
4. Block-diagonal / structured patterns
5. Perturbed versions of your best results

For EACH construction method:
- Run 50-100 seeds with 5k-10k iterations (NOT 15k-50k with 500 seeds!)
- Use numpy.linalg.det for ALL determinant calculations
- Track the best matrix from each method

CRITICAL: Keep TOTAL time per evaluation UNDER 180 seconds. With 20 evaluation budget, you cannot afford:
- 500 seeds × 20k iterations per evaluation
- Bareiss determinant during search

Use the new generate_variants tool to create diverse starting matrices, then refine with SA.

VARIATIONS TO EXPLORE:
- Different initialization methods (random, structured, Paley, Lattice)
- Different SA parameters (T, cool_rate, iterations per seed)
- Different seed counts (5-50, not 500)
- Perturb your best matrix from eval 1 to use as seed for eval 2

RETURNS: The matrix with highest |det(H)| found across ALL construction methods and refinements.
