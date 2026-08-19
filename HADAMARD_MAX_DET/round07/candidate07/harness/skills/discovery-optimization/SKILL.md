---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Focus on PERTURBING base construction (Paley+perturbation, random init) rather than just SA parameter tuning. Test multiple strategies per evaluation with probe, then full eval on best. Use variety in construction seeds and perturbation parameters."
---

# Hadamard Matrix Optimization for n=29 - Strategy Diversity Approach

## THE PROBLEM WITH THE CURRENT APPROACH
The seed achieves 0.545692, and the harness best is only 0.561608. This tiny improvement (0.016) suggests:
- The SA hill climbing on Paley is stuck in a deep local optimum
- Varying SA parameters (T, cool, iterations) on the SAME base matrix doesn't help
- YOU NEED TO CHANGE THE BASE CONSTRUCTION STRATEGY

## CORE STRATEGY: PARALLEL CONSTRUCTION DIVERSITY
Each evaluation should test MULTIPLE base constructions in parallel:

### Construction Strategy A: Paley + Random Perturbation
Start with Paley construction, then randomly flip 5-15% of elements with different seed
Then run SA from this PERTURBED base

### Construction Strategy B: Pure Random Initialization
Start with a random ±1 matrix, then run SA from scratch

### Construction Strategy C: Paley + Targeted Perturbation
Start with Paley, identify rows/cols with lowest |det| contribution, flip elements in those regions

## EVALUATION WORKFLOW (20 evals total)

### Evals 1-5: Test perturbation_fraction variations
- Strategies: Paley+5%, Paley+10%, Paley+15%, Random, Random
- SA params: 10k iterations, T=5.0, cool=0.997
- Perturbation seeds: 0, 100, 200, 300, 400

### Evals 6-10: Test different seed ranges
- Strategies: Paley+10%, Random, Random, Paley+10%, Random
- SA params: 20k iterations, T=10.0, cool=0.995
- Seed ranges: 0-500, 500-1000, 1000-1500, 4000-4500, 8000-8500

### Evals 11-15: Test SA parameter combinations with perturbation
- Strategies: Paley+10%, Paley+10%, Random, Random, Random
- Vary: (T, cool, iters): (3,0.998,15k), (8,0.996,20k), (12,0.994,25k), (5,0.997,20k), (10,0.996,20k)

### Evals 16-20: Best-of-all strategy + refinement
- Take the best-performing strategy from evals 1-15
- Refine with: more iterations, finer perturbation fraction, different SA params

## CRITICAL IMPLEMENTATION NOTES

1. ALWAYS implement MULTIPLE strategies per evaluation, not just one
2. Use PROBE to test 2-3 strategies with 500 iterations each before full eval
3. Track which BASE construction (Paley-perturbed, random, etc.) worked best
4. The perturbation_seed should be VARYED between evaluations (not fixed)
5. NEVER assume Paley is optimal - test random initialization seriously

## Tool Usage

1. probe_solution: Test 2-3 construction strategies with 500 iterations each (500×strategy_count is still cheap)
2. evaluate_solution: Run your BEST strategy from probe with full iterations
3. edit_solution: Provide code with MULTIPLE strategies, return the best one

## Success Criteria
- Score improvement > 0.020 over current harness best (0.561608)
- Evidence that a different base construction strategy outperformed pure Paley
- At least 3 different construction strategies tested in at least 15 evaluations
