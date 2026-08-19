---
name: discovery-optimization
description: "Hadamard 29x29 optimizer. Escape local optima by trying 3-5 different matrix constructions in parallel (Paley, random, low-discrepancy, structured). Use 50-100 seeds with 5k-10k iters each. numpy.linalg.det only. Call generate_variants for diverse starts. Time per eval: <180s."
---

# Hadamard Matrix Optimization - Construction Competition Strategy

## WHY STANDARD SA PARAMETER SWEEPING FAILS
The seed's Paley construction + SA at 500 seeds/15k iters finds a local optimum at det≈0.545.
Parameter tuning alone cannot escape this. You MUST try DIFFERENT construction methods.

## PARALLEL CONSTRUCTION COMPETITION (4-5 methods per evaluation)

### Method A: Paley Construction (quadratic residues mod 29)
Residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j)%29 in residues else -1

### Method B: Random ±1 Matrix
Initialize with random entries, then refine with SA (10-50 seeds, 5k iters)

### Method C: Low-Discrepancy (Sobol-like) Initialization
Use Thue-Morse or Gray code patterns to create balanced ±1 matrix
(approximate: rows alternate patterns to reduce row correlation)

### Method D: Structured Block Construction
Build from smaller blocks with specific patterns

### Method E: Perturbation Search
Start from your BEST matrix found so far, flip entries randomly (5-10 seeds, 5k iters)

## SA Parameter Guidelines
- Iterations per seed: 5,000-10,000 (NOT 15k-50k!)
- Number of seeds: 5-50 (NOT 500!)
- Starting temperature: 2.0-8.0
- Cooling rate: 0.993-0.998

## Determinant Strategy
- ALWAYS use numpy.linalg.det for search (fast, ~0.001s per matrix)
- NEVER use Bareiss during hill climbing (causes timeout)
- Track best |det| across ALL methods and seeds

## Workflow
1. Call generate_variants() to get 4-5 diverse starting matrices
2. For each variant: run 10-30 seeds with 5k-10k SA iterations
3. Track best matrix from each method
4. Use perturbation method E to refine your overall best
5. Call evaluate_solution with the globally best matrix
6. For subsequent evaluations: perturb your best and try new construction

## Budget Management
- Total flips across all methods: ≤ 500,000 (50 seeds × 10k iters × 5 methods)
- Expected time: ≤ 150 seconds with numpy.linalg.det
- NEVER exceed 180 seconds

## Expected Outcome
By exploring multiple construction strategies, you should find matrices with |det| significantly better than the Paley local optimum. Look for 20-50% improvement (score 0.7-0.8+).
