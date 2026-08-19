You are an expert mathematician optimizing a 29x29 +/-1 matrix to maximize |det(H)|. n=29 = 3 mod 4.

KEY INSIGHT: The seed program already has a working Paley construction with good SA parameters. DON'T replace it with inferior methods. Instead: REFINEMENT not expansion.

OPTIMAL STRATEGY for n=29:
1. Start with Paley construction (quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28})
2. Use MULTIPLE cooling schedules tested via probe_solution BEFORE evaluating
3. Apply STRUCTURE-PRESERVING mutations: flip entire rows, flip entire columns, swap two rows, swap two columns
4. These preserve the Hadamard-like structure better than random single flips
5. Run SA with 25k-50k iterations per schedule
6. Total time MUST be <300s per evaluation

PROBE STRATEGY: Test 3-5 variants with different cooling schedules (T=3.0, 5.0, 8.0, 12.0) and mutation types. Pick best for full eval.
NEVER use inferior construction methods (random matrix, perturbed Paley). Focus on refining Paley.
