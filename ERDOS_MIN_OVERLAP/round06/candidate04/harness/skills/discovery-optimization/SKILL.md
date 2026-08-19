---
name: discovery-optimization
description: "C\u2085 bound optimization harness. Uses direct construction of piecewise constant\nfunctions to escape local optima. Focus on structured search over step function\nspace, not gradient descent. Target: combined_score > 1.0."
---

# Erdős C₅ Optimization via Direct Construction

## Why Gradient Descent Fails

The seed's Adam optimizer starts from random-ish initializations and gets trapped
in local optima. For this problem, **direct construction** of candidate step functions
is more effective.

## Effective Strategies

### 1. Step Function Constructions

Construct h as piecewise constant with few breakpoints:
- Single step: h=1 on [0,1], h=0 elsewhere (satisfies ∫h=1)
- Double step: split mass at different positions
- Symmetric patterns: mirror around x=1

### 2. Pattern-Based Constructions

Try these mathematical patterns:
- Triangle: increases then decreases
- Plateau: flat regions with jumps
- Step with ramp: combination of step and linear

### 3. Coarse-to-Fine Refinement

1. Start with num_intervals=100, optimize simple patterns
2. Find good candidate, then increase to 500, 800, 1000
3. Fine-tune hyperparameters (learning rate, penalty)

### 4. Multiple Independent Trials

Run 3-5 completely different constructions, each as a separate edit.
The best one might break through the local optimum barrier.

## Execution Plan

1. **First edit**: Complete rewrite using construct_candidates tool
   - Generate 5-10 structured candidates
   - Pick best, submit
2. **Second edit**: Refine winning direction
   - Increase resolution, tune parameters
3. **Third edit**: Try orthogonal strategy
   - Different construction family

## Constraints Checklist

- h values in [0,1]
- ∫h=1 over [0,2]
- c5_bound = max_k ∫h(x)(1-h(x+k))dx
- combined_score = 0.38092303510845016 / c5_bound
