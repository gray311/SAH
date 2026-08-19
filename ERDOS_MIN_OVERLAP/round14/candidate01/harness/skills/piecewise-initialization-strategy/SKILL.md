---
name: piecewise-initialization-strategy
description: Use construct_valid_step to create valid step function initializations, then test them in the Erdos optimizer.
---

# Piecewise Initialization Strategy

## Step 1: Generate Valid Initializations

Call construct_valid_step with pattern="two_step" or "five_step" to get h_values.
These are GUARANTEED to have integral(h)=1.

## Step 2: Edit the Seed

Replace _get_best_initialization to:
- Take the sigmoid of h_values * 2
- Return this single latent (set num_restarts=1, seed_start=0)

## Step 3: Probe and Evaluate

Call probe_solution to check c5_bound.
If c5_bound < 0.375, call evaluate_solution.

## Step 4: Iterate

If no improvement, call construct_valid_step with different patterns
(three_step, five_step with different weights).
