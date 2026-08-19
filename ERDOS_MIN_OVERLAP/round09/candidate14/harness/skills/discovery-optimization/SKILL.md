---
name: discovery-optimization
description: "Systematic hyperparameter optimization for Erd\u0151s problem. Uses probe_solution for cheap ranking\nof optimizer configs, then full evaluation on promising candidates."
---

# Erdős C5 Optimization - Hyperparameter Tuning Playbook

## Why Hyperparameter Tuning Works

The seed program's 12 initialization patterns already explore diverse starting points.
The real opportunity is tuning the optimizer itself: learning rate schedules, penalty
strengths, restart counts, and discretization resolution can make the difference
between finding C5~0.38 and C5~0.37.

## Step-by-Step Workflow

### Phase 1: Configure Sweep (call hyperparameter_sweep())
- Gets 5 configs varying:
  * Learning rate: 0.001, 0.005, 0.01, 0.02
  * Penalty: 500, 1000, 2500, 5000, 10000
  * Steps: 30k, 50k, 70k
  * Restarts: 1, 2, 3, 5
  * Intervals: 600, 800, 1000

### Phase 2: Probe & Filter
- For each config, run a mini-optimization (500-1000 steps) with probe_solution
- These are CHEAP (~10s vs ~2min for full eval)
- Keep configs where probe c5_bound < 0.38 (i.e., combined_score > 1.0)

### Phase 3: Full Evaluation
- Take top 2-3 configs from probing
- Run full num_steps optimization with evaluate_solution
- Keep the best result

### Phase 4: Refine
- If you beat 0.380923, narrow the sweep around your winning config
- Try: lr ± 50%, penalty ± 20%, steps ± 10%

## Key Principles

- Use probes to filter configs BEFORE spending full evals
- Start broad (large hyperparameter ranges), then narrow down
- Remember: combined_score = 0.38092303510845016 / c5_bound, so you need c5_bound < 0.38
- Save your best program to scratch space between iterations
