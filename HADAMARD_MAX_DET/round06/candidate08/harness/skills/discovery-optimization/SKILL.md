---
name: discovery-optimization
description: "Search 12-15 Paley construction variants with 1-3 element residue perturbations, apply 25k SA iterations to each, return best."
---

# Hadamard Matrix Optimizer for n=29

## Step 1: Generate Perturbed Paley Base Matrices
Standard Paley residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}

Generate 12-15 variations by flipping 1-3 bits in the residue set:
  For each variation:
    - Copy standard residues
    - Randomly flip 1-3 elements (0→1 or 1→0)
    - Build Paley matrix: H[i][j] = 1 if (i-j)%29 in residues else -1

## Step 2: Hill Climb Each Base
For each base matrix (12-15 total):
  - Set current = base.copy()
  - best = current, best_det = det(current)
  - T = 3.0, iterations = 25000, alpha = 0.9965
  - For 25000 iterations:
      * Pick random (i,j)
      * Flip H[i][j]
      * new_det = numpy.linalg.det(H)
      * delta = new_det - current_det
      * If delta >= 0: accept, current_det = new_det
      * Else if T > 1e-15 and random() < exp(delta/T): accept
      * Else: undo flip
      * T *= alpha
      * If new_det > best_det: best = current, best_det = new_det

## Step 3: Return Best
Return the matrix with highest |det| across all 12-15 candidates.

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinants
- NEVER use Bareiss during search
- Generate 12-15 base variants
- Run 25,000 iterations per variant
- Total time < 350 seconds (target: ~15-25 seconds)
