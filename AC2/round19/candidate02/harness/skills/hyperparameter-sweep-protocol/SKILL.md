---
name: hyperparameter-sweep-protocol
description: Systematically explore hyperparameter space for the C2 optimizer.
---

# Hyperparameter Sweep Protocol for C2 Optimization

## Core Principle
The current step-function patterns may be trapped in local optima.
Systematically varying hyperparameters can escape these optima by
changing the search dynamics and resolution.

## Phase 1: Broad Exploration (iterations 1-20)

Step 1: Get Current Parameters
- Call analyze_optimizer_params
- Note baseline values for each hyperparameter

Step 2: Generate Hyperparameter Variants
Create variants by modifying 2-3 key parameters at a time:

Variant Types:
1. HIGH_RESOLUTION: 
   - num_intervals: increase by 30-50% (600 -> 800-1000)
   - num_steps: maintain or increase
   - learning_rate: slightly decrease (0.15 -> 0.1-0.12)

2. LONG_OPTIMIZATION:
   - num_steps: increase by 60-100% (25000 -> 40000-50000)
   - learning_rate: decrease (0.15 -> 0.08-0.1)
   - warmup_steps: increase proportionally

3. SMOOTH_CONVERGENCE:
   - learning_rate: decrease significantly (0.15 -> 0.05-0.08)
   - reinit_std: decrease (0.025 -> 0.01-0.02)
   - reinit_fraction: decrease (0.12 -> 0.05-0.08)

4. AGGRESSIVE_RESTART:
   - reinit_fraction: increase (0.12 -> 0.15-0.20)
   - reinit_std: increase (0.025 -> 0.03-0.05)
   - reinit_interval: decrease (200 -> 100-150)

5. NOVEL_PATTERNS:
   - Change pattern initialization strategy in _create_step_initializer
   - Use patterns with different peak heights and widths
   - Try asymmetric multi-level patterns

Step 3: Probe-Based Ranking
- Call probe_solution on ALL variants (5 probes)
- Rank by probe score
- Call evaluate_solution on TOP 2

Step 4: Iterate
- Track which hyperparameter combinations have been tried
- If no improvement after 2 full evals: try different variants
- Never repeat the same 3 hyperparameters for 5+ iterations

## Phase 2: Focused Refinement (iterations 21-40)

Only if a variant beat the record:
1. Get its hyperparameters via analyze_optimizer_params
2. Make SMALL mutations (+/-10% on each parameter)
3. Probe all variants, evaluate top 1
4. If no improvement after 8 iterations: try different hyperparameter region

## Key Rules
- VARY 2-3 PARAMETERS AT A TIME (not just one)
- Use probes to explore 8-12 combinations before full evals
- Track parameter history to avoid cycling
- Always call analyze_optimizer_params to know current values
