---
name: hadamard-multiple-constructions
description: Specialized skill for n=29 Hadamard optimization. Try MULTIPLE constructions, not just parameter tuning. Use shifted residues, hybrid approaches, extended SA.
---

# Hadamard Matrix Optimization - Multiple Construction Strategies
## Task Maximize |det(H)| for 29x29 ±1 matrix. Seed score: 0.545692.
## CRITICAL FAILURE ANALYSIS The seed approach (Paley + 500 seeds x 15k iters) is too slow and weak: - 7.5M total flips takes 75s, leaving little room for exploration - Many seeds converge to same local optimum - Single-element SA flips are weak in discrete high-dimensional space
## Solution: Multiple Construction Strategies
### Strategy A: Shifted Quadratic Residues Instead of ONE residue set, try SHIFTED versions: - Base: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28} - Shift by k=1,2,3,5,7: add k to each residue mod 29 - Test 5-10 different shifts
For shifted residues: shifted_residues = {(r + k) % 29 for r in base_residues}
### Strategy B: Extended SA (More Iterations, Fewer Seeds) Tradeoff: 200,000 iterations x 3 seeds = 600k flips (~15s) vs 15k x 500 = 7.5M flips (75s) - Fewer seeds reduce redundancy - More iterations per seed escape local optima better
for seed in range(5000, 5030):  # 30 seeds mat = sa(paly, seed, iters=100000, T=10.0, cool=0.996)
### Strategy C: Hybrid Paley + Random Perturbations - Start with Paley matrix - Randomly flip 5-10% of entries - Run SA from perturbed base - Repeat 10 times with different perturbations
### Strategy D: Local Search from Seed 1. Start from seed Paley 2. Evaluate all 841 single flips, flip top 50 3. Evaluate top 200, flip top 20 4. Repeat 3 rounds 5. Run 10k SA from best
## Parameters That Work - Total iterations: 300k-500k (not 7.5M) - Seeds: 3-10 (not 500) - Iterations per seed: 50k-200k - Starting T: 10.0-15.0 - Cool rate: 0.995-0.997
## Tool Usage 1. probe_solution: Test 2-3 strategies (10k iters each) 2. evaluate_solution: Run full strategy (100k+ iters per seed) 3. Always use numpy.linalg.det (fast)
## Expected Outcome With multiple constructions + better SA params, expect score 0.60-0.65.
