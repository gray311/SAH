---
name: discovery-optimization
description: "Hyperparameter-focused optimization of C2 optimizer. Analyze current params, generate concrete code edits for hyperparameters, use probes to rank before full eval."
---

# C2 Optimizer: Hyperparameter Exploration Protocol

## Understanding the EVOLVE-BLOCK
The EVOLVE-BLOCK contains a C2Optimizer class with OptimizerHyperparameters:
- num_intervals: discretization resolution (default 600)
- learning_rate: optimizer step size (default 0.15)
- num_steps: optimization iterations (default 25000)
- warmup_steps: warmup period (default 2500)
- best_c2: current record to beat (0.8962799441554086)
- stagnation_window: detect plateaus (default 100)
- reinit_fraction: restart fraction (default 0.12)
- reinit_std: restart noise std (default 0.025)
- reinit_interval: restart frequency (default 200)

## Phase 1: Hyperparameter Sweep (iterations 1-20)

Step 1: Analyze Current Parameters
- Call analyze_optimizer_params to get current hyperparameter values
- Note which params are at default values

Step 2: Generate Hyperparameter Variants
Create 3-5 variants by modifying hyperparameters:
- Variant A: Increase num_intervals to 800-1000 (higher resolution)
- Variant B: Increase num_steps to 40000-50000 (more optimization)
- Variant C: Decrease learning_rate to 0.05-0.1 (smoother convergence)
- Variant D: Change pattern initialization to patterns 3-10 (novel step patterns)
- Variant E: Adjust reinit_fraction to 0.05-0.15 and reinit_std to 0.01-0.03

Step 3: Probe-Based Ranking
- Call probe_solution on ALL variants (5 probes max per iteration)
- Rank by probe score
- Call evaluate_solution on TOP 2 variants

Step 4: Iterate
- If neither beats record: try different hyperparameter combinations
- Keep track of which hyperparameters are being tried
- Avoid repeating the same 3 hyperparameters for 5+ iterations

## Phase 2: Focused Refinement (iterations 21-40)

Only if a variant beat the record:
1. Analyze its hyperparameters
2. Make SMALL mutations (+/-10% on each hyperparameter)
3. Probe all, evaluate top 1
4. If no improvement after 8 iterations: try completely different hyperparameter region

## Code Edit Examples

# Example 1: Increase resolution and steps
num_intervals: 800
learning_rate: 0.1
num_steps: 40000

# Example 2: Novel pattern initialization (pattern 10)
In _create_step_initializer, use pattern_idx=10:
"Wide base with narrow high peak - heights 1.20, 2.80"

# Example 3: Aggressive reinitialization
reinit_fraction: 0.18
reinit_std: 0.03
reinit_interval: 150

## Key Rules
- Focus on EDITING hyperparameters, not inventing new function families
- Use probes to explore 8-12 hyperparameter combinations before full evals
- NEVER refine the same 3 hyperparameters for 5+ iterations
- Always call analyze_optimizer_params to know current values
