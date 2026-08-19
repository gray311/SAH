---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Try multiple construction strategies (different Paley variants, random bases, hybrid). Use 50k+ iterations, fewer seeds. Always probe before evaluate."
---

# Hadamard Matrix Optimization - Multiple Construction Strategies
## Problem Find 29x29 ±1 matrix maximizing |det(H)|. n=29 ≡ 3 mod 4.
## Seed score: 0.545692 (Paley construction with SA) This is too low. We need better strategies.
## Strategy 1: Multiple Quadratic Residue Sets Instead of ONE residue set, try SEVERAL and pick the best: - Residue set A: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28} (seed) - Residue set B: Shift by k: try k=1,2,3,5,7 (add k to each residue mod 29) - Residue set C: Complementary residues (all non-residues)
For each set, run SA with: 100,000 iterations, 5 seeds, T=10.0, cool=0.996
## Strategy 2: Hybrid Paley + Random Start with Paley, then apply random perturbations: - Take seed Paley matrix - Randomly flip 5-10% of entries - Run SA from this perturbed base: 100k iterations, 3 seeds - Repeat 10 times with different perturbations
## Strategy 3: Extended SA with Fewer Seeds Trade off: 200,000 iterations, 3 seeds - This covers 600k total flips (vs 7.5M in seed) - Each SA run takes ~5 seconds - 3 runs = 15 seconds total
## Strategy 4: Determinant-Gradient Local Search Start from seed Paley, then: 1. Evaluate all single flips (29*29=841 candidates) - use numpy.det 2. Flip top 50 candidates 3. Evaluate these, flip top 20 4. Repeat 3 rounds, keep best 5. Run 10k SA iterations from best
## Implementation Template def construct_hadamard_matrix(n=29, strategy="multiple", **kwargs): # Choose construction method based on strategy # For strategy="multiple": try 3 different residue sets # For strategy="extended": 200k iters, 3 seeds # For strategy="local": gradient-based improvement # ... (implement chosen strategy) return best_matrix
## Key Parameters to Try - Iterations per SA run: 50k, 100k, 200k (seed uses 15k) - Number of seeds: 3, 5, 10 (seed uses 500 - too many!) - Starting temperature: T=5.0, 10.0, 15.0 (seed uses 5.0) - Cool rate: 0.995, 0.996, 0.998 (seed uses 0.9955) - Total flips: aim for 300k-500k (not 7.5M)
## Why Seed Fails 1. 500 seeds × 15k = 7.5M flips takes 75s - too much time 2. Many seeds converge to same local optimum 3. SA with single flips is weak in discrete space 4. Paley construction itself may be suboptimal
## Tool Usage 1. probe_solution: Test 2-3 strategies quickly (10k iters each) 2. evaluate_solution: Run full strategy (100k+ iters) 3. edit_solution: Provide complete working code
## Expected Improvement With better strategies, expect score 0.60-0.65 vs seed 0.545.
