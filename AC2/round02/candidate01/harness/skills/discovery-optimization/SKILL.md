---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize C2 for the second autocorrelation inequality. UNDER THE EVALUATION BUDGET, use probe_solution for cheap ranking of function representations, and representational_probe to systematically explore different function families (step functions, Gaussian mixtures, B-splines, etc.). Diversify exploration rather than tuning a single representation."
---

# C2 Optimization Playbook: Systematic Function Representation Exploration

## Objective
Maximize C2 = ||f * f||2^2 / ((integral(f))^2 ||f * f||_inf). Theoretical max: 1.0. Current record: 0.8963 (step functions).

## Core Principle: Representation > Parameter Tuning
The search space is dominated by FUNCTION FAMILY, not hyperparameters. Before spending evals on tuning, you MUST explore different representations.

## Phase 1: Initial Representation Probe
1. Call representational_probe to understand what function class your current code implements
2. Note the suggestions for alternative representations
3. If not exploring step functions (current record-holders), create a step-function variant immediately

## Phase 2: Probe-Based Exploration (Before ANY Full Eval)
For EACH function family, test 8-10 variants using probe_solution:

### A. Piecewise-Constant (Step Functions)
- Vary: step width (0.1n to 0.9n), number of steps (2-10), heights (1.0-2.0)
- Try: symmetric, asymmetric, multi-level steps
- Expected: Should match or beat 0.8963 baseline

### B. Piecewise-Linear (Current Seed)
- Vary: num_intervals (100, 200, 500), node values, support width
- Try: triangular peaks, trapezoids, multi-modal
- Expected: Smooth transitions, potentially better than steps

### C. Gaussian Mixtures
- Vary: K=2,3,5,10 Gaussians; means=uniform or clustered; sigma=small, medium, large
- Ensure: non-negative (use softplus or exp transformation)
- Expected: Smooth, potentially higher C2 due to better concentration

### D. B-Splines
- Vary: knot positions (uniform, adaptive), coefficients
- Expected: Flexible, local control

### E. Exponential Combinations
- Vary: sum of 2-5 exponentials with different decay rates
- Expected: Natural decay, positive everywhere

## Phase 3: Full Evaluation (After Probing)
1. Select top 3 candidates from probe scores
2. Each: run with MULTIPLE random seeds (2-3 per candidate)
3. Use evaluate_solution for these only
4. Track: which function family performs best

## Phase 4: Deep Dive or Reset
- If top family: increase budget (more intervals, more steps), try ensembles
- If NO improvement: call representational_probe, SWITCH to a completely different function family
- NEVER spend more than 5 evals on the same function family without trying something new

## Critical Success Factors
- Diversify early: First 10-15 probes should cover 4+ function families
- Probe before eval: For each family, probe 8+ variants before 1 eval
- Reset strategy: When stuck at same score for 3 evals, switch function families
- Record keeping: Track which family, which variant, which probe/eval score

## Tool Usage Priority
1. representational_probe — understand current state, get suggestions
2. probe_solution — explore MANY variants cheaply (use liberally!)
3. edit_solution — implement new function class or variant
4. evaluate_solution — confirm top candidates only (budget is limited!)
5. finish — when evals exhausted or no improvement possible
