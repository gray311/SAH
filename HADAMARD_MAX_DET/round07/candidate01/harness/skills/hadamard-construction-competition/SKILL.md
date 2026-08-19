---
name: hadamard-construction-competition
description: Run a parallel construction competition - try 4-5 different matrix generators simultaneously. This beats parameter-only tuning by exploring fundamentally different search landscapes. Use 50-100 seeds per method, 5k-10k iterations.
---

# Hadamard Construction Competition Strategy

## Core Idea: Parallel Search Across Construction Methods
Instead of tuning SA parameters on ONE construction (which gets stuck in local optima),
run 4-5 DIFFERENT matrix generators in parallel. Each explores a different search landscape.

## The 5 Methods (run in parallel per evaluation)

### 1. Paley Construction
- Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- H[i][j] = 1 if (i-j)%29 in residues else -1
- Pros: Mathematically sound for n≡3 mod 4
- Cons: Creates structured patterns that may trap SA

### 2. Random Initialization
- Fill with random ±1 entries
- Pros: Truly diverse starting point
- Cons: High variance, may need more SA iterations

### 3. Thue-Morse Sequence
- Use Thue-Morse pattern (0,1,1,0,1,0,0,1,...) to generate rows
- Pros: Low correlation between rows, good balance
- Cons: May create some structural dependencies

### 4. Van der Corput Lattice
- 1D low-discrepancy sequence for row offsets
- Pros: Systematic space filling, good coverage
- Cons: May create row patterns similar to Thue-Morse

### 5. Perturbation Search
- Start from YOUR BEST matrix found in prior evaluations
- Flip 5-20 random entries, refine with SA (10-30 seeds, 2k-5k iters)
- Pros: Exploits promising regions found earlier
- Cons: Only works if you have a good prior result

## Per-Method SA Settings
- Seeds: 10-30 (NOT 500!)
- Iterations per seed: 5,000-10,000 (NOT 15k-50k!)
- Starting T: 2.0-8.0
- Cooling rate: 0.993-0.998

## Total Budget per Evaluation
- Total flips: 5 methods × 20 seeds × 7,500 iters = 750,000 (should be < 800k)
- Expected time: 150-180 seconds with numpy.linalg.det
- Target: Stay under 180 seconds

## Workflow
1. Call generate_variants() to get diverse starting matrices
2. For each variant: run 10-30 SA seeds with 5k-10k iterations
3. Track best |det| from each method
4. Use perturb_best() to create variants from your overall winner
5. Call evaluate_solution with the globally best matrix
6. Next eval: start perturb_best from this result + try a new construction

## Expected Outcome
By exploring 5 different landscapes in parallel, you'll find the method that escapes
the Paley local optimum. Expect 20-50% improvement over seed score (target: 0.7-0.8+).

## Critical Rules
- ALWAYS use numpy.linalg.det for search (never Bareiss!)
- Total time MUST be < 180 seconds
- Track best matrix from EACH method, not just average
- Perturbation search (method 5) is crucial for exploiting good finds
- After eval 1: use perturb_best on your winner for all subsequent evals
