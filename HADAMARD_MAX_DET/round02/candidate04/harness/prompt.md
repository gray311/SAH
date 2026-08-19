You are optimizing a program to find a 29x29 matrix with entries +/-1 that maximizes the absolute determinant.

KEY MATH FACT: For n=29 (which is 3 mod 4), the Paley construction creates a Hadamard-like matrix using the Legendre symbol. The correct construction is:
- Compute Legendre symbol (a/29) for each offset a = (i-j) mod 29
- H[i][j] = +1 if (i-j) mod 29 is a quadratic residue mod 29, else -1
- Quadratic residues mod 29 are: 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28

CRITICAL: The seed program's Paley implementation has a BUG - it doesn't properly handle the Legendre symbol. You MUST use the correct construction.

Strategy:
1. FIRST: Use probe_solution to quickly test different construction approaches
2. Try the CORRECT Paley construction (using Legendre symbol properly)
3. Then apply hill climbing with MANY iterations (15000-20000) and proper annealing
4. Use multiple independent restarts (10-15 seeds)
5. Before any full evaluation, probe 3-5 variants and only evaluate the best
6. Always stay under 200 seconds total runtime

Tools: edit_solution, evaluate_solution, probe_solution, finish
