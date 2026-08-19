---
name: discovery-optimization
description: "Multi-restart optimization for Erdos minimum overlap."
---

# Erdos Minimum Overlap - Multi-Restart Strategy

## Why the Seed Fails
The seed program tries 12 initialization patterns but:
- Uses identical hyperparameters for all
- Runs a single long optimization (59000 steps) per start
- Doesn't probe before final evaluation

This means all 12 starts go through the SAME optimization trajectory, missing diverse basins.

## The Winning Approach
Implement a 5-restart loop inside _optimize_single_run:

### Step 1: Define 5 Distinct Initializations
Use these patterns:
- Pattern 0: Bimodal at 0.25, 0.75 with Gaussian peaks
- Pattern 1: Triangular 3-level piecewise
- Pattern 2: Periodic alternating high/low
- Pattern 3: Golomb-inspired (5 marks at 0.25, 0.7, 1.1, 1.75)
- Pattern 4: Sine-wave modulated

### Step 2: Multi-Restart Loop
For each pattern:
1. Generate latent vector
2. Normalize to ensure integral(h)=1
3. Run 2-phase optimization: 3000 steps (LR=0.05, penalty=5000) + 10000 steps (LR=0.01, penalty=20000)
4. Call probe_solution to get c5_bound (cheap!)
5. Track best 2 by probe

Vary num_intervals in [400, 800, 1200] across restarts.

### Step 3: Final Evaluation
After multi-restart, use evaluate_solution on top 2 candidates.
Return the best c5_bound found.
