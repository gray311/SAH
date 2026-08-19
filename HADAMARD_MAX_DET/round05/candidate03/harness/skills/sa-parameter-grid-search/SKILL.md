---
name: sa-parameter-grid-search
description: Systematic SA parameter exploration for Hadamard det maximization. Grid search over iterations, temperature, cooling rate, and seed count.
---

# SA Parameter Grid Search for Hadamard n=29

## Objective
Find optimal SA parameters to maximize |det(H)| from Paley construction.

## Parameter Space to Explore
Create a grid covering:
- iterations: [20000, 30000, 40000, 25000]
- initial_temp: [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
- cool_rate: [0.995, 0.996, 0.997, 0.998]
- num_seeds: [3, 4, 5, 6]

## Strategy
1. Use quick_local_search (15k iters) to quickly rank parameter combinations
2. Test 8-10 key combinations from the grid
3. Pick top 2 by probe score
4. Run full evaluation on best one
5. If score improves, expand grid around winning parameters
6. If not, try escape perturbations

## Key Combinations to Test First
A. Low temp, moderate iter: 20k iters, T=2.0, cool=0.995, 3 seeds
B. Medium temp, high iter: 40k iters, T=5.0, cool=0.996, 5 seeds
C. High temp, low iter: 20k iters, T=7.0, cool=0.995, 3 seeds
D. Balanced: 30k iters, T=4.0, cool=0.997, 4 seeds
E. Aggressive cooling: 25k iters, T=3.0, cool=0.998, 4 seeds
F. Slow cooling: 40k iters, T=6.0, cool=0.996, 6 seeds
G. Very low temp: 30k iters, T=2.0, cool=0.998, 3 seeds
H. High temp extended: 40k iters, T=7.0, cool=0.995, 5 seeds

## After Grid Search
From top 2 parameter sets:
1. Try escape A: checkerboard flip then 15k SA (T=5.0)
2. Try escape B: random 30% flip then 15k SA (T=5.0)
3. Try escape C: band flip (|i-j| in [5,10]) then 15k SA (T=5.0)

## Final Refinement
From best escape, run:
- Coarse: T=10.0, cool=0.999, 5k iters
- Fine: T=1.0, cool=0.998, 20k iters

Keep best across all searches.
