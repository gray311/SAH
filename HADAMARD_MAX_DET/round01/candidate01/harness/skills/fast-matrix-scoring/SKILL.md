---
name: fast-matrix-scoring
description: Quick scoring techniques for ±1 matrices. Use when you need many evaluations fast. Combine with probe_solution for strategy ranking. Use analyze_hadamard_construction to understand your current approach.
---

# Fast Scoring for Hadamard Matrices

## Determinant Computation Options
1. **Bareiss Algorithm**: Exact integer determinant, O(n³). For n=29, ~24,389 ops per det.
   - Advantages: Exact, no precision errors
   - Disadvantages: Slow if called many times

2. **LU Decomposition with Integer Arithmetic**: Similar to Bareiss, ~same speed.

3. **Circulant Matrix Exploitation**: If your construction has structure, compute det via eigenvalues.

## Optimization Tips

- **Pre-compute**: If iterating over seeds, share common computations
- **Batch Evaluation**: Process multiple candidate matrices in parallel if possible
- **Early Termination**: If |det| stops improving for 100 iterations, consider aborting

## When to Use Fast Scoring
- probe_solution is always preferred over full scoring for strategy ranking
- Use full scoring only when:
  - You need exact score for submission
  - probe_solution indicates strong potential
  - You're at end of probe budget

## Avoid
- Re-computing determinant more than necessary
- Calling full eval on every parameter variation
- Using expensive operations inside evaluation loops

## Score Interpretation
- For n=29, |det| in range 10^12 to 10^17 is expected
- Higher |det| is always better (no minimum threshold)
- Validity: matrix must be 29×29 with all entries ±1
- If validity=0, fix the structural issue first before optimizing det
