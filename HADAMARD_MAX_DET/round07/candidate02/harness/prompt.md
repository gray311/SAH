You are optimizing a 29×29 ±1 matrix to maximize |det(H)|.

CRITICAL INSIGHT: The seed uses a fixed Paley construction from quadratic residues.
SA hill-climbing from this single seed often gets trapped in a local optimum.

Your strategy must break this trap by:

1. PER-EVALUATION: Try MULTIPLE diverse starting matrices (not just one SA run):
   - 3 runs from perturbed Paley (flip 5-10 random entries in the base)
   - 2 runs from random ±1 matrices
   - Keep the original Paley as 1 run
   Total: 6 runs × 2000 iterations × numpy.det ≈ 12 seconds per eval (easily under 350s)

2. Use probe_solution FIRST to test 3-5 diverse parameter sets before full evaluate

3. When editing, provide COMPLETE working code that:
   - Implements the base Paley construction exactly: residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   - Adds perturbation: randomly flip 5-15 entries in the base matrix
   - Adds random start: initialize with random ±1 values
   - Runs MULTIPLE SA chains in parallel per evaluation
   - Uses numpy.linalg.det for ALL determinant calculations (never Bareiss in search)

4. Budget: 20 evals. Aim for diverse strategies that explore different regions of matrix space.

5. Stop when you find a matrix with det > seed best, or exhaust budget.
