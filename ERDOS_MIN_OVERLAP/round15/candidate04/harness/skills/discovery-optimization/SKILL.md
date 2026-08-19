---
name: discovery-optimization
description: "Optimize the seed's 12 existing initialization patterns by enforcing integral constraint and running full optimization on each. Use probes to filter constraint violations before spending evals."
---

# Erdos Optimizer - Pattern Refinement Strategy

## Problem
The seed has 12 initialization patterns. Most fail the integral constraint or give high c5_bound.

## Solution
Don't create new patterns - make the existing 12 work better.

## Workflow

### Step 1: Constraint Enforcement Edit
Edit _get_best_initialization to:
- Take a single pattern's latent
- Scale it so integral(h)=1: latent_scaled = latent / jnp.sum(latent)
- Pass through sigmoid to get h in [0,1]

### Step 2: Screen with Probes
For each of the 12 patterns:
1. EDIT seed to use only that pattern
2. CALL probe_solution to check: integral(h)≈1 and c5_bound estimate
3. If integral constraint violated or c5_bound >= 0.38, SKIP this pattern
4. If c5_bound < 0.38, KEEP for full evaluation

### Step 3: Full Optimization
For patterns passing probe:
- EDIT seed to run FULL optimization (keep 59000 steps, multi-restart)
- CALL evaluate_solution
- Record combined_score

### Step 4: Refine Best Pattern
If any pattern improves:
- EDIT seed to use ONLY that successful pattern's structure
- TUNE hyperparameters: increase num_intervals (1600), adjust learning_rate
- CALL evaluate_solution

## Expected Outcome
- At least one of the 12 patterns should pass probe
- Full optimization should find c5_bound < 0.38
- combined_score > 1.0
