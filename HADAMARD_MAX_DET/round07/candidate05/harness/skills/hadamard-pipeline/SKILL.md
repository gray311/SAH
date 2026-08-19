---
name: hadamard-pipeline
description: Specialized skill for n=29 Hadamard construction. Uses multi-construction pipeline (Paley, random, block, permuted) with structural refinements (row swaps, 2x2 block flips, cyclic shifts). NO simulated annealing. 3-4 constructions times 50 refinements each.
---

# Hadamard Construction Pipeline - Multi-Strategy

## Goal
Maximize |det(H)| for 29x29 ±1 matrix using diverse constructions, NOT SA.

## Constructions to Try
### 1. Paley Construction
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

### 2. Random Matrix
Generate 29x29 with random +/-1 entries.

### 3. Block Pattern
Create a 4x4 pattern and extend to 29x29.

### 4. Permuted Paley
Take Paley, randomly permute rows and columns, then flatten.

## Refinement Operations (50 per construction)

Op A: Swap Row i with Row j
Swap rows i and j, recompute det.

Op B: Swap Col i with Col j
Swap columns i and j, recompute det.

Op C: Flip 2x2 Block
Pick random position (r,c), flip H[r][c], H[r+1][c], H[r][c+1], H[r+1,c+1]
Recompute det.

## Algorithm

best_score = 0
best_matrix = None

Try 4 constructions. For each:
  For step in 0..49:
    Pick random op from {A, B, C}
    Apply op to current matrix
    det = abs(numpy.linalg.det(matrix))
    if det > best_score:
      best_score = det
      best_matrix = matrix

Return best_matrix

## Key Rules
- NO simulated annealing loops with 10k+ iterations
- Exactly 50 refinements per construction
- 4 constructions total = 200 total refinements
- Each refinement: 1 op + 1 det computation (~0.001s)
- Total time: ~30s, well under 350s
- Use numpy.linalg.det, NOT Bareiss
