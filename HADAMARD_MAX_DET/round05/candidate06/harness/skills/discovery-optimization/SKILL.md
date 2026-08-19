---
name: discovery-optimization
description: "Block-based Hadamard optimizer for n=29. Start from Paley, then use block-coordinate\ndescent with 3x3/5x5/7x7 block flips. Add orthogonality enhancement and circular\nrow/column shifts. Run 4 parallel searches with numpy determinant. Total under 180 seconds."
---

# Block-Based Hadamard Optimization for n=29

## Why Simple Simulated Annealing Fails
Simulated annealing with single-bit flips cannot escape the local optima created by
the Paley construction for n=29. The search needs COORDINATED block-level changes.

## Core Algorithm: Block Coordinate Descent
Instead of flipping one entry at a time, flip entire blocks of entries:

Block sizes: 3x3, 5x5, 7x7

For each iteration:
1. Choose a block size from {3, 5, 7}
2. Randomly select a top-left corner position (row, col)
3. Create a candidate matrix by flipping all entries in that block
4. Compute determinant of candidate
5. Accept if candidate has higher determinant OR with probability exp(delta/T)

## Search Configurations (run all 4 in parallel)

Config A: Small blocks (3x3)
  - Seeds: 5 different seeds
  - Iterations per seed: 20000
  - Cooling schedule: start T=5.0, cool_rate=0.995

Config B: Medium blocks (5x5)
  - Seeds: 5 different seeds
  - Iterations per seed: 15000
  - Cooling schedule: start T=8.0, cool_rate=0.994

Config C: Large blocks (7x7)
  - Seeds: 5 different seeds
  - Iterations per seed: 15000
  - Cooling schedule: start T=10.0, cool_rate=0.993

Config D: Circular shifts
  - For each shift amount s in {1,2,3,4,5}:
    - Take Paley construction
    - Circularly shift each row i by s positions
    - Run 3000 iterations of single-entry flips to fine-tune
  - Use 1 seed per shift, T=3.0, cool_rate=0.998

## Orthogonality Enhancement Phase
After the block search:
1. Compute for each pair of rows (i,j): correlation = dot product of row i and row j
2. Identify the pair with highest absolute correlation
3. Flip a random 3x3 block in one of those two rows
4. Repeat 5-10 times

## Implementation Details
- Start from Paley construction:
  Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
  H[i][j] = 1 if (i-j) mod 29 is a quadratic residue, else -1

- Determinant: Always use numpy.linalg.det (fast, ~0.001s per call)
- Never use Bareiss during search (causes timeout)

- Total time estimate:
  Config A: 5 seeds x 20k iters x 15ms = 1.5s
  Config B: 5 seeds x 15k iters x 15ms = 1.1s
  Config C: 5 seeds x 15k iters x 15ms = 1.1s
  Config D: 5 shifts x 3k iters x 15ms = 0.2s
  Total: ~4s (well under 350s budget)

- Use complete working code in EVOLVE-BLOCK
- Return the matrix with maximum absolute determinant
