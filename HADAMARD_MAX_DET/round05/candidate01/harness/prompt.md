You are an expert mathematician optimizing a 29x29 +/-1 matrix to maximize |det(H)|.
n=29 = 3 mod 4, so use Paley construction (quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28})
as your PRIMARY starting method.

CRITICAL: You have 350 seconds per evaluation. Your code must COMPLETE within this budget.
Generate ONE focused optimization strategy, not 4+ methods in parallel.

STRATEGY: Start with correct Paley construction, then use SIMULATED ANNEALING with:
- 50,000 iterations (not more!)
- Initial temperature: 10.0
- Cooling rate: 0.9985
- Random seed: try seeds [42, 123, 456] and pick the best result

AFTER generating your solution, call analyze_matrix_structure to check your matrix quality.
If analysis shows high row correlation or poor orthogonality, make targeted mutations to improve.

NEVER call probe_solution unless you have multiple parameter variations to compare.
Use evaluate_solution only on your best single candidate.

Remember: Complete working code that runs in <300s. Use numpy.linalg.det for all determinant calculations.
