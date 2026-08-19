---
name: discovery-optimization
description: "Step function construction for Erdos C5 minimization. Generate explicit step-function candidates with structure, probe them cheaply, then evaluate the best. Focus on: uniform step patterns, delta-peak patterns, and bipartite step patterns. Avoid random gradient-based optimization."
---

# Step Function Construction for Erdos Problem

## Core Principle
The seed optimizer uses gradient descent from random latent vectors. This finds local minima. Instead, **construct explicit step functions** with structure that naturally minimizes overlap.

## Step 1: Generate Structured Candidates
CALL propose_step_function to get 5 structured candidates:
- uniform_steps: equal-height steps
- delta_peaks: narrow peaks at strategic positions
- bipartite: high on [0,a), low on [a,2]
- tri-bipartite: high-low-high pattern at [0,0.3), [0.3,0.7), [0.7,2]
- sinusoidal_steps: sin/cos-based step patterns

## Step 2: Probe and Filter
For each candidate, CALL probe_solution:
- Keep only if c5_bound < 0.375 (allow margin)
- Typically 2-3 candidates pass

## Step 3: Evaluate Best Candidates
CALL evaluate_solution on the best 2-3 candidates from step 2.

## Step 4: Structural Mutation (if stuck)
If no improvement after step 3:
1. Look at the best h from evaluate_solution
2. Identify step boundaries (where h jumps)
3. Create variants: shift one boundary, split a wide step into two, merge adjacent steps
4. CALL probe_solution on variants
5. CALL evaluate_solution on best variant

## Expected Outcome
With explicit step-function construction, we should find c5_bound < 0.37 quickly. The gradient optimizer gets stuck; structured construction finds different basins.
