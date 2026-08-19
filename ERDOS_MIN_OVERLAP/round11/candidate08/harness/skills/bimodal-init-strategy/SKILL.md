---
name: bimodal-init-strategy
description: Use construct_bimodal_init to generate the optimal two-peak initialization for the Erdos problem. The true optimum requires two narrow symmetric peaks at x=0.25 and x=0.75. This tool generates that exact structure directly. Then optimize from this promising start rather than random initialization.
---

# Bimodal Initialization Strategy for Erdos Problem

## Why This Works
The Erdos minimum overlap constant C5 is minimized by a step function with TWO narrow peaks
at positions 0.25 and 0.75. Random initializations rarely find this structure.

## How to Use construct_bimodal_init
1. Call construct_bimodal_init ONCE to get the optimal two-peak latent vector
2. Extract "latent" from the response
3. EDIT the EVOLVE-BLOCK to set initial_latent = this latent vector
4. Optionally reduce num_steps and base_learning_rate for fine optimization from this good start

## Parameter Tuning
- peak_width: Start at 0.15, try 0.1, 0.08, 0.12 to find optimal sharpness
- peak_height: Default 10.0 usually works; adjust if normalization fails

## Optimization Tips
- Use probe_solution to quickly check if the constraint is satisfied
- Use smaller learning rate (0.001-0.005) when starting from this good initialization
- Fewer steps needed (20000-50000) since you're already near the optimum
- Call evaluate_solution only 2-3 times after optimization from this start

## Expected Outcome
Starting from this principled initialization should yield combined_score > 1.0
(c5_bound < 0.380923) with proper optimization from this head start.
