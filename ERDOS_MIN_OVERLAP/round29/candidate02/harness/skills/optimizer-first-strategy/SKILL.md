---
name: optimizer-first-strategy
description: Run the seed optimizer on diverse initializations. The optimizer's 59000 steps are where improvement happens.
---

# Optimizer-First Strategy for Erdos C5

## Core Principle
The seed optimizer ALREADY finds near-optimal solutions (combined_score=0.99997).
Don't bypass the optimizer - IMPROVE ITS SEEDS, then let it train.

## Step-by-Step Workflow

1. CALL generate_optimizer_seeds()
   - Generates 10 diverse latent-space initializations
   - Each designed for the 59000-step JAX training loop

2. FOR EACH of the 10 seeds:
   - CALL edit_solution to set EVOLVE-BLOCK's initial latent to this seed
   - CALL evaluate_solution to run the full optimizer
   - Record combined_score

3. PICK THE BEST result across all seeds
   - If any combined_score > 1.0, FINISH immediately
   - If all <= 1.0, proceed to Phase 2

4. Phase 2 (only if Phase 1 fails): Try hyperparameter variations
   - num_intervals: 400, 1600, 3200
   - base_learning_rate: 0.001, 0.01
   - penalty_strength: 30, 100

## Critical Rules
- ALWAYS run the optimizer's 59000-step training - this is where improvement happens
- Don't waste evals on precomputed patterns
- Generate seeds ONCE, then run optimizer on each
- If optimizer finds combined_score > 1.0, finish immediately
