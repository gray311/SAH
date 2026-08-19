---
name: hadamard-matrix-optimization
description: Task-specific skill for maximizing |det(H)| of 29x29 ±1 matrix. n=29 has no true Hadamard, so use combinatorial optimization with multiple construction methods (Paley, cyclic shifts) and extended search.
---

# Hadamard-like Matrix Optimization for n=29

## Task: Maximize |det(H)| for 29x29 matrix with entries ±1

## Key mathematical insight
True Hadamard matrices require n to be 1, 2, or a multiple of 4.
For n=29, we cannot achieve the theoretical max of n√n = 29√29 ≈ 155.5.
We need combinatorial optimization to find near-optimal matrices.

## Construction methods to try (in order)

Method 1: Paley construction (best for n ≡ 3 mod 4)
Quadratic residues mod 29: {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
For each entry (i,j): H[i][j] = 1 if (i-j) mod 29 is quadratic residue, else -1
Add diagonal correction: H[i][i] should be +1

Method 2: Cyclic shifts
Start with any 29x29 ±1 matrix (e.g., from Method 1)
Generate additional rows by cyclically shifting the first row
H[i] = shift(H[0], i * k) for some shift amount k

Method 3: Random perturbations with annealing
Start from structured matrix
For t = 1 to 10000:
  Randomly flip one entry
  Calculate determinant (Bareiss for exact, or numpy for fast check)
  Accept if |det| improves, else with prob exp((|new|-|old|)/T)
  Schedule: T = 0.8 / (1 + t * 0.0008)

Method 4: Multi-start optimization
For seed in range(5, 15):
  Generate starting matrix (Paley or random)
  Run hill climbing from this seed
  Track best result

## Implementation tips

- Use Bareiss algorithm for exact integer determinant (avoids floating point errors)
- Total search time MUST be < 200 seconds per evaluation
- Try at least 2 different construction methods per evaluation
- Use fast_det_probe to quickly check direction before probe_solution
- Use probe_solution to rank variants before evaluate_solution

## Workflow

1. Choose construction method (start with Paley + multi-start)
2. Set iterations = 5000-10000, restarts = 5-10
3. Write/edit code for this specific configuration
4. Call edit_solution, then evaluate_solution
5. If score is good, try parameter variations
6. Before next evaluate, probe 2-3 variants
7. Evaluate only the probe winner
8. Repeat or finish
