---
name: direct-construction-playbook
description: Build step functions directly from mathematical insights, not via gradient descent. Use simple piecewise constants that satisfy ∫h=1, then probe/rank them.
---

# Direct Construction Strategy for C5 Optimization

## Why Gradient Descent Fails Here
The landscape has many local optima. The seed's Adam optimizer gets stuck.
Better: construct informed candidates analytically.

## Construction Recipes

### 1. Single Step Function
h(x) = 1 if x ∈ [0,1], else 0
- Integral: 1×1 = 1 ✓
- This is a baseline; often suboptimal but easy to compute

### 2. Symmetric Double Step
h(x) = 0.5 if x ∈ [0,0.5] ∪ [1.5,2], else 0
- Integral: 0.5×0.5 + 0.5×0.5 = 0.5 ✓ (need to scale)
- Actually: h=1 on [0,0.5]∪[1.5,2] gives integral=1 ✓

### 3. Three Equal Steps
Divide [0,2] into 3 parts, put h=1 on two parts
- Integral: 1×(4/3) > 1, so use h=0.75 on two thirds

### 4. Concentrated Mass
Place most of the mass in the center [0.75,1.25]
- May reduce overlap with shifted versions

### 5. Sinusoidal Approximation
h(x) ≈ 0.5 + 0.5×sin(π(x-1)) shifted to be positive
- Discretize carefully to get ∫h=1

## Workflow
1. Generate 3-5 candidates using these recipes
2. Call probe_solution on each to get cheap scores
3. Rank and evaluate top 2-3
4. If needed, refine with gradient descent from promising starts

## Key Insight
Direct construction > random initialization + gradient descent
Mathematical structure beats brute force search
