---
name: adaptive-hyperparam-schedule
description: Adaptive hyperparameter scheduling for non-convex optimization. Scales learning rate and penalty based on training phase.
---

# Adaptive Hyperparameter Scheduling for Erdős Optimization

## Principle
Fixed hyperparameters cause premature convergence or insufficient exploration. 
Dynamic scheduling adjusts exploration (lr, penalty) based on training phase.

## Three-Phase Schedule
Phase 1 (steps 0-20k): lr = 0.01, penalty = 500
Phase 2 (steps 20k-30k): lr = 0.001, penalty = 5000
Phase 3 (steps 30k-59k): lr = 0.0001, penalty = 10000

## Implementation in edit_solution
In the EVOLVE-BLOCK, after optimizer.init(), create a phase-aware training loop:

Phase detection: phase = step // 10000
- Phase 0 (0-19k): use lr=0.01, penalty=500
- Phase 1 (20k-29k): use lr=0.001, penalty=5000
- Phase 2 (30k-59k): use lr=0.0001, penalty=10000

Update optimizer with phase-specific params each iteration.

## Why This Works
- Early phase explores diverse h shapes, finds good local minima
- Mid phase refines shape while maintaining constraint
- Late phase enforces integral=1 exactly, final polish
- Combined with seed's 12-pattern init: systematic coverage

## Budget Awareness
With 20 evals, use probe_solution for ranking (3-5 variants), 
evaluate_solution only for top 2-3. Each eval costs budget.
