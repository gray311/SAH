---
name: discovery-optimization
description: "Direct piecewise constant initialization to beat the seed''s latent-based approach."
---

# Direct Step Function Construction for Erdos Optimizer
## Core Strategy
Replace the seed's _get_best_initialization with a DIRECT step function construction. The seed uses latents + sigmoid, but we can encode h(x) directly as a piecewise constant function.
## Step 1: Define the Pattern
Use a 3-level step function: - Region 1: [0, a] where h=1 - Region 2: [a, 2-a] where h=b (0 < b < 1) - Region 3: [2-a, 2] where h=0
Constraint: integral(h) = a + b*(2-2a) = 1
## Step 2: Choose Parameters
Try a=0.4, solve for b: 0.4 + 2b - 0.8b = 1 0.4 + 1.2b = 1 b = 0.5
So: h=1 on [0,0.4], h=0.5 on [0.4,1.6], h=0 on [1.6,2]
## Step 3: Edit the Seed
Replace _get_best_initialization to directly return the discretized step function (no latent, no sigmoid).
## Step 4: Evaluate
Call evaluate_solution. If combined_score > 1.0, success!
