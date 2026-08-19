---
name: discovery-optimization
description: "Erd\u0151s C5 optimization with adaptive hyperparameter scheduling. Leverages seed's 12-pattern init, adds phase-based learning schedules, and uses probe-based ranking."
---

# Erdős C5 Optimization Strategy

## Problem
Minimize: max_k integral h(x)(1-h(x+k))dx for h: [0,2]→[0,1] with integral h=1

## Why Seed's 12 Patterns Work
The seed tries 12 patterns: random Gaussian, uniform, sine combinations, 
bimodal splits at 0.5/1.0/2/3/1/3, concentrated regions. These produce 
diverse h shapes that when sigmoided and normalized satisfy integral h=1 reasonably.

## Enhancement: Adaptive Scheduling
Seed uses fixed hyperparameters. Add three-phase schedule:

Phase 1 (steps 0-20000): lr=0.01, penalty=500 (exploration)
Phase 2 (steps 20000-30000): lr=0.001, penalty=5000 (refinement)
Phase 3 (steps 30000-59000): lr=0.0001, penalty=10000 (fine-tuning)

## Workflow with scan_hyperparams()
1. Call scan_hyperparams() to get hyperparameter configs
2. For each config, edit EVOLVE-BLOCK to:
   - Keep seed's 12-pattern initialization
   - Add adaptive optimizer loop with phase-based scheduling
   - Run 3 restarts per config
3. Use probe_solution to score all variants
4. Evaluate top 2-3 with evaluate_solution
5. Iterate with new hyperparams

## Key Edit: Add Training Scheduler
After optimizer init in EVOLVE-BLOCK, add phase-aware training loop that 
adjusts lr and penalty based on current step phase (0-19k, 20k-29k, 30k+).

## Tool: scan_hyperparams
Returns systematic hyperparameter configs. Call ONCE at start.
