---
name: discovery-optimization
description: "Focused 29x29 Hadamard optimizer using Paley construction + focused simulated annealing. 50k iterations, 3 seeds, analyze matrix structure for targeted improvements."
---

# Focused 29x29 Hadamard Optimization

## Task
Maximize |det(H)| for a 29x29 matrix with entries +/-1.

## Step 1: Correct Paley Construction
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For each entry H[i][j]:
  diff = (i - j) mod 29
  H[i][j] = 1 if diff in quadratic_residues else -1

## Step 2: Simulated Annealing Refinement
- Initial matrix: Paley construction
- Iterations: 50,000 total
- Temperature schedule: Start T=10.0, cool_rate=0.9985
- Mutations: Randomly flip one entry at a time
- Acceptance: Always accept improvements; accept worsening with prob exp(-delta/T)
- Track best result across all iterations
- Use 3 different random seeds [42, 123, 456], keep best

## Step 3: Matrix Structure Analysis
After generating your matrix, analyze it using analyze_matrix_structure:
- Check row orthogonality (correlations should be near 0)
- Check condition number indicators
- Identify high-correlation row pairs to target for mutation

## Step 4: Targeted Mutation (if needed)
If analysis shows issues:
- For high-correlation rows: try flipping entries where rows differ
- Run 10,000 additional iterations with T=5.0, cool_rate=0.999
- Use same deterministic seed for reproducibility

## Step 5: Final Validation
- Compute determinant with numpy.linalg.det
- Ensure all entries are exactly +/-1 (integers)
- Return the complete matrix

## BUDGET WARNING
- Total runtime MUST be < 300 seconds
- numpy.linalg.det on 29x29 is fast (~0.001s)
- 50,000 iterations with numpy det takes ~50 seconds
- 3 seeds = 150 seconds, plus analysis = ~160 seconds

## COMMON ERRORS TO AVOID
- Multiple construction methods (Paley, random, etc.) in one evaluation
- More than 50,000 iterations (causes timeout)
- More than 3 seeds (does not fit in budget)
- Using Bareiss determinant (causes timeout, use numpy)
- Not checking matrix structure before finalizing
