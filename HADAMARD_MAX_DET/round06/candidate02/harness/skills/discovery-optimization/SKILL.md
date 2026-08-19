---
name: discovery-optimization
description: "Paley Hadamard optimizer for n=29. Build matrix from quadratic residues, run 6 parallel hill climbs of 15k iters each with T=3.0, cool=0.997. Add perturbation phase. Use probe_solution to screen variants before evaluate."
---

# Paley Hadamard Optimizer for n=29

## Step 1: Build 6 Paley Base Matrices
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}

For each seed in [1,2,3,4,5,6]:
  - Build Paley matrix with random seed
  - Set this as base matrix for this run

## Step 2: Parallel Hill Climbing
For each of the 6 bases:
  - Set best_det = det(base), best_mat = base
  - Set T = 3.0
  - For 15,000 iterations:
      * Pick random (i,j), flip H[i,j]
      * new_det = numpy.linalg.det(H)
      * delta = new_det - best_det
      * If delta > 0: accept flip, best_det = new_det
      * Else if T > 1e-10 and random() < exp(delta/T): accept flip
      * Else: undo flip
      * T *= 0.997
      * If new_det > best_det: best_det = new_det, best_mat = H.copy()
  - Store result (best_mat, best_det) for this seed

## Step 3: Perturbation Phase
- Take the BEST result from Step 2
- Make 100 random ±1 flips to create perturbed matrix
- Run 5,000 more hill climbing iterations with T=2.0, cool=0.998
- Track best during this phase

## Step 4: Return Best
Return the matrix with highest determinant across all phases.

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinant computations during search
- Total runtime MUST be < 180 seconds
- Always use exactly 6 starting seeds for parallel hill climbs
- DO NOT use Bareiss during search
