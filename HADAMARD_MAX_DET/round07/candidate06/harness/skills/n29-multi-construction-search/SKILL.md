---
name: n29-multi-construction-search
description: Specialized skill for n=29 Hadamard optimization using parallel construction testing. Implements 4 strategies in parallel with 3-5 seeds each, 10k-15k iterations per seed. Uses numpy.linalg.det for fast search, completes each eval in ~15 seconds.
---

# Multi-Construction Hadamard Search for n=29

## OVERVIEW
Test 4 construction strategies in parallel with 3-5 seeds each, 12k iterations per seed.
Total: ~5 seeds × 4 strategies × 12k iters = 240k operations per eval.
Time: ~15 seconds per eval (vs 75s with 500 seeds).

## FOUR CONSTRUCTION STRATEGIES

### 1. Paley Construction (Baseline)
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

### 2. Random Initialization
Random ±1 matrix, hill climb from there. Good for escaping local optima.

### 3. Perturbed Paley
Start with Paley, flip 5-10 random entries. Tests sensitivity to initialization.

### 4. Alternative Residue Patterns
Try different quadratic residue selections. May find better patterns.

## EXECUTION PLAN (per evaluation):

Initialize:
- n = 29
- best_overall_det = 0
- best_overall_matrix = None

For seed in range(3, 8):  # 5 seeds
    seed_rand = Random(seed)
    
    # Strategy 1: Paley
    paley_mat = build_paley()
    for iter in range(12000):
        result = sa_hillclimb(paley_mat, seed_rand, iters=1)
        det = abs(np.linalg.det(np.array(result, dtype=float)))
        if det > best_overall_det:
            best_overall_det = det
            best_overall_matrix = result
    
    # Strategy 2: Random
    rand_mat = build_random()
    for iter in range(12000):
        result = sa_hillclimb(rand_mat, seed_rand, iters=1)
        det = abs(np.linalg.det(np.array(result, dtype=float)))
        if det > best_overall_det:
            best_overall_det = det
            best_overall_matrix = result
    
    # Strategy 3: Perturbed Paley
    pert_mat = build_perturbed_paley()
    for iter in range(12000):
        result = sa_hillclimb(pert_mat, seed_rand, iters=1)
        det = abs(np.linalg.det(np.array(result, dtype=float)))
        if det > best_overall_det:
            best_overall_det = det
            best_overall_matrix = result

Return best_overall_matrix

## DETINENT CALCULATION:
- ALWAYS use numpy.linalg.det for SEARCH
- ~0.001s per 29×29 matrix
- NEVER use Bareiss during search (causes timeout)

## EXPECTED OUTCOME:
With 20 evaluations × 4 strategies × 5 seeds, you explore 400 construction paths.
Even with 12k iterations each, this covers much more search space than 500 seeds on one strategy.

## CHECKLIST:
- ✅ 4 strategies implemented (Paley, Random, Perturbed, Alt)
- ✅ 3-5 seeds per evaluation
- ✅ 10k-15k iterations per seed per strategy
- ✅ numpy.linalg.det for all scoring
- ✅ Track best across all strategies
- ✅ Return only the best matrix
