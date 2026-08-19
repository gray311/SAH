---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Try MULTIPLE construction methods (Paley, random, perturbed Paley). Use probe_solution to test parameters before evaluating. \nKey: Use numpy.linalg.det, not Bareiss during search."
---

# Hadamard Matrix Optimizer for n=29

## Task
Find a 29×29 matrix with entries ±1 that maximizes |det(H)|.

## Construction Methods to Try
Since the Paley construction alone may be trapped in a local optimum, try these methods:

### Method A: Paley Construction
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For H[i][j]: diff = (i-j) mod 29
H[i][j] = 1 if diff in residues else -1

### Method B: Random ±1 Matrix
Start with random ±1 entries

### Method C: Perturbed Paley
Start with Paley, then flip K random entries (K = 5-20)

## Search Strategy
For each method:
- Run simulated annealing with simulated annealing
- Try multiple (temperature, cooling_rate, iterations_per_seed) combinations
- Use numpy.linalg.det for all determinants (fast)

## CRITICAL: Use probe_solution
- Call probe_solution with 5-10 different parameter sets
- Parameters to vary: T (1-10), cool_rate (0.99-0.999), iterations (10k-100k), num_seeds (3-12), construction_method
- Use approximate scores to rank variants
- Pick the top 2-3 variants for full evaluate_solution

## Implementation
- Write complete code that implements ALL methods
- Return the best matrix found
- MUST complete in <300 seconds
- Use numpy.linalg.det exclusively during search

## Workflow per evaluation
1. Implement code with all 3 construction methods
2. Test with probe_solution (use 20 probes for fine-grained search)
3. Evaluate the best variant with evaluate_solution
4. If score improves, iterate with different parameters
