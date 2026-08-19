---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Use 3-5 seeds max, parallel construction testing (Paley, random, perturbed), \n10k-20k iterations per construction. Fast evaluations (~15s) enable exploring many more strategies."
---

# Hadamard Matrix Optimization for n=29 - Multi-Construction Strategy

## CRITICAL CHANGE: Few Seeds, Many Constructions

The seed's 500-seed approach is TOO EXPENSIVE. You only have 20 evaluations total.
**Use 3-5 seeds per evaluation** and test MULTIPLE constructions in parallel.

## Construction Strategies to Try (implement ALL in one evaluation):

### Strategy A: Paley Construction
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

### Strategy B: Random Initialization
Random ±1 matrix, then hill climb from there

### Strategy C: Perturbed Paley
Start with Paley, flip 5-10 random entries, then hill climb

### Strategy D: Alternative Residue Patterns
Try different quadratic residue subsets or patterns

## For EACH strategy:
- Run 3-5 SA seeds with 10,000-15,000 iterations each
- Use numpy.linalg.det for fast scoring
- Track the best matrix from this strategy

## Final Result:
Return the BEST matrix across all strategies you tested.

## Why This Works:
- 500 seeds × 15k iters × ~0.001s/det = ~75 seconds per eval (TOO SLOW)
- 5 seeds × 15k iters × ~0.001s/det = ~15 seconds per eval (MUCH BETTER)
- With 15s evals, you can do 30+ evaluations, exploring 3x more strategies

## Tool Usage:
- edit_solution: Provide COMPLETE code implementing ALL 4 strategies in parallel
- probe_solution: Test different iteration counts (10k vs 15k) quickly
- evaluate_solution: Run full parallel search with best parameters
