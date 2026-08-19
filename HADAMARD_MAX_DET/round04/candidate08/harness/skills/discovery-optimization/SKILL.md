---
name: discovery-optimization
description: "Paley-focused Hadamard optimizer for n=29. Use correct Paley residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.\nSimulated annealing with 5 seeds, 3 cooling schedules (T=10/5/2, cool_rate=0.998/0.996/0.994),\n20k iterations/seed, numpy det. Probe 3 variants before evaluate."
---

# Hadamard n=29 Paley Optimizer

## Paley Construction
Residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

## Simulated Annealing
- 5 seeds: [42, 123, 456, 789, 2024]
- 3 cooling schedules (probe to select best):
  A. T=10.0, cool=0.998 (20k iters)
  B. T=5.0, cool=0.996 (20k iters)
  C. T=2.0, cool=0.994 (20k iters)
- Use numpy.linalg.det (fast, ~0.001s per matrix)
- NEVER use Bareiss during search (causes timeout!)

## Workflow
1. Generate Paley matrix
2. For each seed and each cooling schedule: run SA, track best det
3. Call probe_solution to test 3 schedule variants
4. Call evaluate_solution on best probe variant
5. If score improves, try different seeds or refine cooling

## Budget
- Total iterations: 5 seeds × 20k × 3 schedules = 300k flips
- Expected time: ~30 seconds (well under 350s)
- Use probe to pre-rank, evaluate only 1 variant
