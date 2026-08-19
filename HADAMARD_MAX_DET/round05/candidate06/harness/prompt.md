You are optimizing a 29x29 +/-1 matrix to maximize abs(det(H)). n=29 is 3 mod 4.

CRITICAL: Simple simulated annealing with single-bit flips FAILS for n=29.
The seed program gets stuck in local optima immediately.

YOU MUST implement a BLOCK-BASED SEARCH with these phases:

PHASE 1 - STRUCTURED INITIALIZATION:
Start from a Paley construction (quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}),
but also try cyclic shifts of rows and columns.

PHASE 2 - BLOCK COORDINATE DESCENT:
Instead of flipping single entries, flip entire BLOCKS of entries (3x3, 5x5, or 7x7).
For each candidate block flip, compute determinant change and accept using Metropolis criterion.

PHASE 3 - ORTHOGONALITY ENHANCEMENT:
After block search, explicitly maximize orthogonality by perturbing rows with highest
off-diagonal correlations in H^T H.

PHASE 4 - ESCAPE VIA CIRCULAR SHIFTS:
Try circular shifts of entire rows by s positions where s is 1 to 5.

BUDGET: ~25k iterations total with numpy determinant. You have 350 seconds per evaluation.
Run 4 independent searches with different block-size strategies.

NEVER use Bareiss during search (timeout risk). Always use numpy.linalg.det.
