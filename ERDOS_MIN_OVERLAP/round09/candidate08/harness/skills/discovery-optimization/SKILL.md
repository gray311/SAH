---
name: discovery-optimization
description: "Systematic hyperparameter search over principled step function constructions for Erd\u0151s minimum overlap. Use one construction at a time with grid search over intervals, learning rate, penalty, and steps. Validate with probe before full evaluation."
---

# Erdős Minimum Overlap - Hyperparameter Search Strategy

## Problem
Minimize max_k ∫ h(x)(1-h(x+k)) dx for h: [0,2]→[0,1] with ∫h=1.

## Core Insight
The seed program (800 intervals, lr=0.0053, penalty=1370) achieves near-optimal. 
To beat it, we need: (1) different construction patterns, (2) aggressive hyperparameter variation.

## Method: Systematic Search

### Step 1: Pick ONE Construction Type

**bimodal**: Two symmetric peaks
h(x) = sigmoid(α1 * exp(-(x-0.25)²/(2σ1²)) + α2 * exp(-(x-0.75)²/(2σ2²)))

**periodic**: Duty-cycle based
h(x) = sigmoid(β * (1 - 2 * rect(x/T)))

**Golomb**: Peaks at optimal ruler positions
h(x) = sigmoid(Σ γ_i * exp(-(x-x_i)²/(2σ_i²)))
where x_i = [0.25, 0.625, 0.9375, ...]

### Step 2: Grid Search Hyperparameters

For your chosen construction, try:
- num_intervals: 400, 800, 1600 (higher = more flexible, slower)
- base_learning_rate: 0.001, 0.01, 0.05, 0.1 (higher = faster convergence, risk of overshoot)
- penalty_strength: 1000, 5000, 10000, 20000 (higher = stricter integral=1 constraint)
- num_steps: 30000, 50000, 80000 (more steps = better optimization)

### Step 3: Use probe_solution

For each (construction, hyperparams) combo:
1. Generate the EVOLVE-BLOCK edit
2. Call probe_solution to get approximate c5_bound (~10s, separate budget)
3. Track which combos give best probe scores

### Step 4: Full Evaluation

Take top 1-2 candidates from probe ranking:
1. Make the same edit
2. Call evaluate_solution for exact score

### Step 5: Iterate

- If no progress after 5 iterations, perturb your best parameters by 20 percent
- Try a different construction type
- Never generate multiple constructions in one edit

## Common Pitfalls

- Don't try to implement 4 constructions at once - you'll break the optimizer
- Don't use the same hyperparameters as seed - small perturbations won't help
- DO use probe_solution to eliminate bad configs quickly
- DO keep each edit focused on ONE parameter change
