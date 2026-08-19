---
name: discovery-optimization
description: "Shorten training and reduce complexity to escape seed local optimum. Perturb seed initialization, reduce penalty strength, try smaller num_intervals."
---

# Escaping Seed Local Optimum

## Problem
The seed optimizer trains 59000 steps on complex patterns (num_intervals=800). It gets stuck at the seed score of 0.999968.

## Solution: Simplicity First

1. REDUCE training to 3000-5000 steps for quick feedback
2. Reduce penalty_strength from 61.0 to 10-20
3. Try num_intervals=100, 200, or even 50 for simpler step functions
4. Use SGD or AdamW instead of default optimizer
5. Generate 5-6 diverse mutations of seed parameters

## Workflow

Batch 1 (evals 1-3):
- Edit: num_steps=3000, penalty_strength=15.0, num_intervals=200, seed_start=1
- Edit: num_steps=5000, penalty_strength=10.0, num_intervals=100, seed_start=2
- Edit: num_steps=4000, penalty_strength=20.0, num_intervals=150, seed_start=3

Batch 2 (evals 4-6):
- If no improvement, try num_intervals=50 (very coarse)
- Try penalty_strength=5.0 (very weak constraint)
- Try seed_start=4 with different random seed

## Why This Works
- Simpler programs (fewer intervals, shorter training) escape local optima faster
- Weaker penalty allows more flexibility
- Multiple seeds prevent convergence to same solution
seed_pattern = "sigmoid(jnp.array([-0.5, -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0]))"
