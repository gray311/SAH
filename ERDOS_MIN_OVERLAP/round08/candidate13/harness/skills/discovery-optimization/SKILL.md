---
name: discovery-optimization
description: "C5 bound optimization via discrete construction.\nAbandon gradient descent; try explicit piecewise constant functions.\nUse probe to rank variants cheaply. Target combined_score > 1.0."
---

# C5 Optimization: Discrete Construction

## Problem
Minimize: max_k integral_0^2 h(x)(1-h(x+k))dx
Constraints: h in [0,1], integral_0^2 h(x)dx = 1

## Why Gradient Descent Fails
The seed's Adam optimizer gets trapped in local optima on this non-convex problem.

## Discrete Construction Approaches

1. **Single block**: h=1 on [0,1], 0 elsewhere
2. **Uniform**: h=0.5 everywhere  
3. **Two symmetric bumps**: centered at x=1
4. **Three equal blocks**: equal width regions
5. **Concentrated**: narrow peak at center
6. **Oscillatory**: alternating regions

## Workflow
1. Generate 5-10 candidates using different constructions
2. Call probe_solution on each (~30 probes)
3. Rank by probe score
4. Evaluate top 1-2 with evaluate_solution
5. If combined_score > 1.0, success!

## Constraints
- integral of h must equal exactly 1
- h must stay in [0,1]
