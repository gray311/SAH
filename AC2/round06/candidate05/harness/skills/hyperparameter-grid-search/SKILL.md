---
name: hyperparameter-grid-search
description: Method playbook for C2 optimization using systematic hyperparameter sweeping in the multi-start framework. Probe 4+ configs before eval, max 4 evals.
---

# C2 Optimization: Hyperparameter Grid Search

## Objective
Maximize C2 > 1.02872. Current baseline: 1.02872 (seed). Target: surpass this.

## Strategy: Systematic Hyperparameter Sweeping

The seed program uses a multi-start optimization framework. The key to improvement is tuning hyperparameters, not rewriting the entire optimization.

### Hyperparameter Grid

#### num_intervals: 150, 250, 350, 500, 700
- Purpose: Controls discretization resolution
- Hypothesis: Finer resolution (500-700) better approximates optimal step functions
- Trade-off: More intervals = more parameters to optimize, slower convergence

#### learning_rate: 0.05, 0.1, 0.125, 0.15, 0.2
- Purpose: Step size in gradient descent
- Hypothesis: Higher LR (0.15-0.2) escapes local minima; lower LR (0.05-0.1) finds smoother convergence
- Seed uses: 0.125

#### stagnation_window: 50, 100, 200, 300
- Purpose: How many steps before reinitialization kicks in
- Hypothesis: Larger window (200-300) preserves good solutions; smaller window (50-100) escapes local minima faster
- Seed uses: 100

#### reinit_fraction: 0.05, 0.1, 0.11, 0.15, 0.2
- Purpose: Fraction of function to perturb during reinitialization
- Hypothesis: Higher fraction (0.15-0.2) diversifies search; lower fraction (0.05-0.1) preserves good solutions
- Seed uses: 0.11

#### num_steps: 20000, 30000, 40000, 50000
- Purpose: Total optimization steps
- Hypothesis: More steps (50000) finds better local minima; fewer steps (20000-30000) may find global optimum faster
- Seed uses: 40000

#### reinit_std: 0.01, 0.015, 0.02, 0.025, 0.03
- Purpose: Standard deviation of reinitialization noise
- Hypothesis: Higher std (0.025-0.03) diversifies more; lower std (0.01-0.015) is more conservative

## Execution Protocol

### Phase 1: Configuration Generation (1 iteration)
1. Call hyperparameter_sweeper with seed_num=0,1,2,3,4
2. Get 5 diverse hyperparameter configurations
3. Each config specifies all optimizer hyperparameters

### Phase 2: Probe-Based Ranking (2-3 iterations)
1. For each of the 5 configs, call probe_solution
2. Record probe scores and rank configurations
3. Select TOP 2 configurations by probe score

### Phase 3: Full Evaluation (1-2 iterations)
1. For each of the TOP 2 configs, call evaluate_solution
2. Track which hyperparameters yielded improvement
3. If still no improvement after 2 evals, try different hyperparameter combinations

### Phase 4: Deep Dive or Reset
- If top configuration shows promise: refine hyperparameters around that point (try 1-2 adjacent values)
- If no improvement after 4 evals: SWITCH strategy (try polynomial decay, Gaussian mixtures, or the seed's original multi-start with original hyperparams)

## Critical Success Factors
- Probe 4+ hyperparameter configurations BEFORE any full evaluation
- Maximum 4 full evaluations total
- Use hyperparameter_sweeper for structured grid search
- Systematic exploration beats random mutations
- Track which hyperparameter combinations worked best
- Diversify: try different num_intervals with different learning_rates

## Tool Usage Priority
1. hyperparameter_sweeper - generate concrete hyperparameter configs
2. probe_solution - rank many configurations cheaply
3. evaluate_solution - confirm only top 2 candidates
4. finish - when evals exhausted or score > 1.02872 achieved
