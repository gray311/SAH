---
name: discovery-optimization
description: "Hyperparameter grid search for C2 optimizer. The seed has 11 step patterns; tune optimizer hyperparameters (learning_rate, num_intervals, num_steps, reinit_fraction, stagnation_window) to find better search dynamics. Use probes to filter before full eval."
---

# C2 Optimizer: Hyperparameter Tuning Protocol

## Core Insight
The seed program has 11 diverse step-function patterns (sufficient diversity).
The issue is the optimizer's SEARCH DYNAMICS. Tune hyperparameters to find
better convergence to a higher C2 constant.

## Tunable Hyperparameters (change ONE at a time initially)
1. learning_rate: 0.05-0.3 (seed: 0.15) - affects step size in gradient descent
2. num_intervals: 400-1200 (seed: 600) - resolution of discretization
3. num_steps: 15000-50000 (seed: 25000) - optimization budget
4. reinit_fraction: 0.05-0.2 (seed: 0.12) - how much to reinitialize on stagnation
5. stagnation_window: 50-500 (seed: 100) - when to trigger reinitialization

## Phase 1: Grid Search (iterations 1-12)

Step 1: Generate 3-5 variants with ONE changed parameter each:
- Variant A: learning_rate = 0.05 (smaller steps for stability)
- Variant B: learning_rate = 0.3 (larger steps for exploration)
- Variant C: num_intervals = 400 (coarser, faster convolutions)
- Variant D: num_intervals = 1200 (finer resolution)
- Variant E: num_steps = 15000 (less budget, test convergence)
- Variant F: num_steps = 50000 (more budget, test overfitting)
- Variant G: reinit_fraction = 0.05 (less aggressive reinit)
- Variant H: reinit_fraction = 0.2 (more aggressive reinit)
- Variant I: stagnation_window = 50 (frequent reinit)
- Variant J: stagnation_window = 500 (rare reinit)

Step 2: Probe ALL variants (up to 30 probes available)
- Call probe_solution on each variant
- Record probe scores

Step 3: Evaluate TOP 1-2 by probe score
- If probe score > 1.0 (beats seed), this is promising
- Full eval gives true C2 score

Step 4: If both full evals fail or scores < 1.0:
- Generate 5 MORE variants with different parameters
- Continue probing until iteration 12 or a winner found

## Phase 2: Focused Tuning (iterations 13-25)

Only if Phase 1 found at least one variant with combined_score > 1.0:

1. Analyze which hyperparameters helped most:
   - If higher learning_rate worked: try 0.2, 0.25, 0.3
   - If finer num_intervals worked: try 800, 1000, 1200
   - If more num_steps worked: try 35000, 40000, 50000
   - etc.

2. Generate 3 fine-grained variants around the winning region:
   - Variant A: +/- 20% on each promising parameter
   - Variant B: try different combinations (e.g., lr=0.25 + steps=40000)
   - Variant C: try boundary values (min/max of promising ranges)

3. Probe all, evaluate top 1-2

4. If no improvement after 5 iterations: go back to Phase 1

## Key Rules
- NEVER generate complete programs from scratch - edit the OptimizerHyperparameters class
- ALWAYS change at least one hyperparameter from seed values
- Use probes aggressively (up to 30) to filter before full eval
- If probe < 1.0, skip full eval and try different hyperparameters
- Focus on SEARCH DYNAMICS, not function architecture (seed has enough diversity)
