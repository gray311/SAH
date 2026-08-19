---
name: discovery-optimization
description: "Multi-phase Hadamard optimizer: test multiple constructions (Paley, random, structured),\nhill-climb each with numpy.det, use probe_solution to rank variants, evaluate only the best."
---

# Multi-Phase Hadamard Matrix Optimizer for n=29

## PHASE 1: Construction Methods
Test these initialization strategies:

A. Paley Construction (recommended first):
   Residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
   For H[i][j]: diff = (i-j) mod 29
     H[i][j] = 1 if diff in residues, else -1

B. Random Initialization:
   Fill matrix with random ±1 entries

C. Structured Perturbation:
   Start with Paley, flip 10-20% of entries randomly

## PHASE 2: Hill Climbing for Each Construction
For each construction method:
  - Run 3-5 different random seeds
  - For each seed: 5,000-10,000 simulated annealing iterations
  - Temperature: start at 3.0, cool by 0.996 per iteration
  - Use numpy.linalg.det for ALL determinant calculations during search
  - Track best determinant found

Simulated Annealing Parameters:
  - Flip one random element at each iteration
  - Accept if delta > 0, or with probability exp(delta/T) if delta < 0
  - After acceptance, update best if new > best

## PHASE 3: Strategy Selection with Probing
Use probe_solution to test 3-5 variant configurations:
  - Variant 1: Paley + 5k iters, T=3.0, cool=0.996, 3 seeds
  - Variant 2: Random init + 10k iters, T=2.0, cool=0.997, 3 seeds
  - Variant 3: Perturbed Paley + 5k iters, T=3.0, cool=0.995, 3 seeds

Call probe_solution on these variants, pick the winner, then call evaluate_solution on it.

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinants during search (NOT Bareiss)
- Total search time must be < 350 seconds
- Use probe_solution BEFORE evaluate_solution to save budget
- Try 3-5 construction methods in parallel, pick the best
- Expected iterations per variant: 5,000-10,000 (NOT 100,000)
