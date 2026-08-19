---
name: discovery-optimization
description: "Systematically sweep hyperparameters in the multi-start optimization framework. Test num_intervals, learning_rate, stagnation_window, reinit_fraction in combination. Probe 4+ configs before evaluating. Target >1.02872."
---

# C2 Optimization: Hyperparameter Sweeping Strategy

## Objective
Maximize C2 > 1.02872. Current baseline: 1.02872 (seed). Target: surpass this.

## Key Insight
The seed program already implements a multi-start optimization framework with step-function initializations. The breakthrough comes from tuning hyperparameters, not rewriting the entire optimization.

## Hyperparameter Grid to Explore

### num_intervals: 150, 250, 350, 500, 700
- Seed uses 350
- Hypothesis: Finer resolution (500-700) may better approximate optimal step functions
- Alternative: Coarser (150-250) may converge faster and avoid local minima

### learning_rate: 0.05, 0.1, 0.125, 0.15, 0.2
- Seed uses 0.125
- Hypothesis: Higher LR (0.15-0.2) may escape shallow local minima
- Alternative: Lower LR (0.05-0.1) may find smoother convergence

### stagnation_window: 50, 100, 200, 300
- Seed uses 100
- Hypothesis: Larger window (200-300) prevents premature reinitialization
- Alternative: Smaller window (50-100) may escape local minima faster

### reinit_fraction: 0.05, 0.1, 0.11, 0.15, 0.2
- Seed uses 0.11
- Hypothesis: Higher fraction (0.15-0.2) diversifies search more
- Alternative: Lower fraction (0.05-0.1) preserves good solutions longer

### num_steps: 20000, 30000, 40000, 50000
- Seed uses 40000
- Hypothesis: More steps (50000) may find better local minima
- Alternative: Fewer steps (20000-30000) may find global optimum faster

## Execution Protocol

### Phase 1: Configuration Generation
1. Call hyperparameter_sweeper with diverse seeds to get 4-5 configurations
2. Each config specifies: num_intervals, learning_rate, stagnation_window, reinit_fraction, num_steps

### Phase 2: Probe-Based Ranking
1. For each of 4-5 configurations, call probe_solution
2. Record probe scores and rank configurations
3. Select TOP 2 configurations by probe score

### Phase 3: Full Evaluation
1. For each of the TOP 2 configs, call evaluate_solution (full run)
2. Track which hyperparameters yielded improvement
3. If still no improvement after 2 evals, try different hyperparameter combinations

### Phase 4: Deep Dive (if needed)
- If top configuration shows promise: refine hyperparameters around that point
- If no improvement after 4 evals: SWITCH strategy (try polynomial decay or Gaussian mixtures)

## Critical Success Factors
- Probe 4+ configurations BEFORE any full evaluation
- Maximum 4 full evaluations total
- Use hyperparameter_sweeper for structured exploration
- Systematic grid search beats random mutations
- Track which hyperparameter combinations worked best

## Tool Usage Priority
1. hyperparameter_sweeper - generate concrete hyperparameter configs
2. probe_solution - rank many configurations cheaply
3. evaluate_solution - confirm only top 2 candidates
4. finish - when evals exhausted or score > 1.02872 achieved
