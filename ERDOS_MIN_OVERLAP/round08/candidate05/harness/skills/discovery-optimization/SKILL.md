---
name: discovery-optimization
description: "C5 bound optimization via constructive search. Replaces gradient-based latent\noptimization with explicit piecewise constant construction and local search.\nTarget: combined_score > 1.0."
---

# Constructive C5 Optimization

## Why Gradient Methods Fail

The seed uses Adam on a sigmoid latent, but:
- The objective max_k ∫ h(x)(1-h(x+k)) dx is non-convex
- The constraint ∫h=1 is a hard boundary
- Gradients are noisy from FFT-based correlation

## Constructive Strategy

### Step 1: Simple Base Functions

Start with explicit piecewise constant h:
- h(x) = 1 on [0,1], 0 elsewhere → ∫h=1 ✓
- h(x) = 0.5 on [0,2], ∫h=1 ✓
- Alternating: 0.75 on [0,0.5], 0.5 on [0.5,1], 0.25 on [1,1.5], 0 on [1.5,2]

### Step 2: Local Search

For each candidate h:
- Try swapping adjacent interval boundaries
- Adjust interval widths (maintain ∫h=1)
- Perturb h values within [0,1] keeping integral=1

### Step 3: Pattern Families

- **Uniform blocks**: h=α on [0,a], 0 elsewhere, choose α=1/a
- **Bimodal**: mass concentrated at two points
- **Centered**: symmetric around x=1
- **Staggered**: shifting blocks to minimize overlap

### Step 4: Evaluation

For each constructed h:
1. Verify: 0≤h≤1, ∫h=1 (within tolerance)
2. Compute c5_bound using FFT correlation
3. Track best c5_bound

## Implementation Notes

- Use numpy arrays for explicit h representation
- Compute integral as sum(h) * dx
- Use FFT for efficient correlation
- Local search: try 5-10 perturbations per candidate
- Budget: use evaluations strategically, don't waste on infeasible candidates
