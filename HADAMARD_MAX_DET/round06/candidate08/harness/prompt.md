You are optimizing a 29x29 ±1 matrix to maximize |det(H)|.
n=29 ≡ 3 mod 4, so use Paley-type constructions with quadratic residues.

## YOUR STRATEGY: Search the Construction Space
The seed uses the standard Paley construction with residues R = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.
DO NOT treat R as fixed. Instead:

1. Generate MULTIPLE candidate base matrices by PERTURBING the Paley construction:
   - Flip bits in R (try 12-18 different residue sets, each differing by 1-3 elements)
   - For each residue set, build the Paley matrix and then apply hill climbing
   - Each full search (building + hill climbing) must complete in <350 seconds

2. For each base matrix candidate:
   - Copy the matrix
   - Run 20,000-30,000 simulated annealing iterations (T=3.0, cool_rate=0.9965)
   - Track the best determinant found

3. Return the matrix with the highest |det| across ALL candidates.

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinants during search (fast, ~0.001s per matrix)
- NEVER use Bareiss during search (causes timeout)
- Generate at least 12 different base constructions (flip 1-3 bits in residues)
- Total runtime MUST be < 350 seconds (target: ~15-30 seconds)
- Call edit_solution with COMPLETE working code implementing this strategy
- Call evaluate_solution once per evaluation
- Use probe_solution to test different numbers of base candidates before full evaluation
