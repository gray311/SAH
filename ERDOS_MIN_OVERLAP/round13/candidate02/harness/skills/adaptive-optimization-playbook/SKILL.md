---
name: adaptive-optimization-playbook
description: Use adaptive refinement with warm strong training followed by gradual annealing to escape local minima.
---

# Adaptive Optimization for Erdos Problem

## Key Insight

The seed program has good initializations (12 patterns). The bottleneck is OPTIMIZATION QUALITY, not initialization.

## Two-Phase Strategy

### Phase 1: Warm Strong Optimization

Use adaptive-refine with:
- base_lr: 0.1-0.5 (strong learning)
- num_steps: 2000-5000 (intensive training)
- penalty_strength: 50-100 (enforce constraint)

This escapes local minima through aggressive optimization.

### Phase 2: Fine-Tuning

Use adaptive-refine again with:
- base_lr: 0.01-0.05 (gentle refinement)
- num_steps: 5000-10000 (polishing)
- penalty_strength: 100-200 (tight constraint)

This fine-tunes the solution.

## Workflow

1. Start with seed program (no edit, or small hyperparameter tweak)
2. Call adaptive-refine with strong parameters
3. Call evaluate_solution on result
4. If no improvement, try different seed_start values (0, 5, 10)
5. If still stuck, try different penalty_strength values
