---
name: batch-training-screening
description: Systematically train all 15 seed patterns and screen analytically. Only evaluate best candidates.
---

# Batch Training and Screening for Erdos Problem

## Workflow

1. CALL train_and_probe_batch (with temperature=0.5, penalty_strength=60.0)

2. The tool trains all 15 patterns with 3 restarts each

3. Results are returned sorted by c5_bound (lowest first)

4. CALL evaluate_solution on the TOP 2-3 candidates (lowest c5_bound)

5. If no improvement, call train_and_probe_batch with modified hyperparameters

## Why This Works

- Explores FULL pattern space (15 patterns x 3 restarts = 45 trained candidates)
- Lightweight training (1 gradient step per restart) finds better local minima
- Analytical c5_bound screening after training is more accurate
- Budget-efficient: 1 tool call + 2-3 evals

## Expected Results

Find c5_bound < 0.38 candidates quickly through systematic exploration.
