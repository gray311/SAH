---
name: discovery-optimization
description: "Paley+SA optimizer for n=29. Focus on SA parameter exploration (iter, temp, cool_rate, seeds). Use quick_local_search to rank variants. Try checkerboard/ random/ band perturbations as escapes. Total < 300s."
---

# Hadamard n=29 Optimizer: SA Parameter Exploration

## Task
Maximize |det(H)| for 29×29 ±1 matrix using Paley construction + simulated annealing.

## BASE APPROACH: Paley Construction
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
H[i][j] = 1 if (i-j) mod 29 in residues, else -1

## Phase 1: SA Parameter Grid Search (MUST DO FIRST)
Test these combinations (use quick_local_search, 15k iters each):

| Variants | iterations | initial_temp | cool_rate | num_seeds |
|----------|------------|--------------|-----------|-----------|
| A | 20000 | 2.0 | 0.995 | 3 |
| B | 20000 | 4.0 | 0.997 | 4 |
| C | 20000 | 6.0 | 0.996 | 5 |
| D | 30000 | 3.0 | 0.998 | 4 |
| E | 30000 | 5.0 | 0.997 | 5 |
| F | 40000 | 2.5 | 0.998 | 3 |
| G | 40000 | 7.0 | 0.996 | 6 |
| H | 25000 | 4.5 | 0.997 | 4 |

Call quick_local_search with all 8 variants. Pick TOP 2 by probe score.

## Phase 2: Targeted Escapes from Phase 1 Best
For each of top 2, try these escapes (15k iters, temp=5.0, cool=0.992):
- Escape A: Start from best, flip all where (i+j) % 4 == 0, then SA
- Escape B: Start from best, flip 30% of entries randomly, then SA
- Escape C: Start from best, flip where 5 <= |i-j| <= 10, then SA

Pick best result from escapes.

## Phase 3: Final Refinement
From Phase 2 best, run two more SA runs:
- Run X: T=10.0, cool=0.999, 5000 iters (broad exploration)
- Run Y: T=1.0, cool=0.998, 20000 iters (fine tuning)

Keep best from all searches.

## Implementation Checklist
1. ✓ Implement correct Paley construction with residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
2. ✓ Implement 8-parameter-variant SA grid
3. ✓ Implement 3 escape patterns
4. ✓ Use numpy.linalg.det for ALL hill climbing
5. ✓ Call quick_local_search on all 8 variants first
6. ✓ Total time < 300s
7. ✓ Use all 20 evals if exploration continues to improve

## CRITICAL
- NEVER use Bareiss during search (causes timeout)
- Use quick_local_search to rank before calling evaluate_solution
- Keep all SA runs within 250s total
