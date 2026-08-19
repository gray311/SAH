---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Use multiple strategies: (1) SA from Paley with 5 seeds, T=2.0/cool=0.996/50k iters; (2) Block-level SA with single+2x2 flips; (3) Random start SA; (4) Paley+row/col swaps. Total <180s."
---

# Hadamard Matrix Optimizer for n=29

## Task
Find a 29×29 matrix with entries ±1 that maximizes |det(H)|.

## Base Construction: Paley Matrix
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For H[i][j]: diff = (i-j) mod 29; H[i][j] = 1 if diff in residues, else -1

## Critical: Try MULTIPLE Strategies per Evaluation

### Strategy A: SA from Paley (Primary)
- Start: Paley base matrix
- T = 2.0, cool_rate = 0.996
- Iterations: 50,000
- Seeds: [1000, 2000, 3000, 4000, 5000] (5 seeds)
- Mutation: Flip ONE random element per iteration
- Accept if det improves OR exp(delta/T)
- Keep best across all 5 seeds

### Strategy B: Block-level SA
- Start: Paley base matrix
- T = 1.5, cool_rate = 0.995
- Iterations: 10,000
- Mutation: 
  * 70%: Flip ONE random element
  * 30%: Flip all 4 elements in a random 2×2 block
- Accept if det improves OR exp(delta/T)

### Strategy C: Random start
- Start: Random ±1 matrix (each entry ±1 with prob 0.5)
- T = 3.0, cool_rate = 0.997
- Iterations: 30,000
- Seeds: 2 different random seeds
- Mutation: Flip ONE random element

### Strategy D: Paley + Perturbation
- Start: Paley base
- Row swaps: Swap 2 random rows, 10 times (revert after each)
- Col swaps: Swap 2 random columns, 10 times (revert after each)
- T = 1.0, cool_rate = 0.998
- Iterations: 20,000
- Seeds: 2

## Determinant Calculation
- ALWAYS use numpy.linalg.det (fast, ~0.001s per matrix)
- NEVER use Bareiss during search (causes timeout)

## Budget Management
- Total runtime < 180 seconds per evaluation
- If any strategy exceeds 50s, reduce iterations proportionally
- Use probe_solution to test 2-3 strategy variants BEFORE evaluate_solution
- Evaluate only the winner

## Workflow
1. Implement all 4 strategies
2. Run them in parallel (threading or process)
3. Collect best determinant from each strategy
4. Return the matrix with highest determinant
5. Use probe_solution to validate parameter choices before final evaluate
