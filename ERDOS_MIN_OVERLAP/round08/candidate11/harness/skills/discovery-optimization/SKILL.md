---
name: discovery-optimization
description: "C\u2085 bound optimization via constructive search. Focus on explicit step function designs rather than gradient descent. Targets combined_score > 1.0."
---

# Erdős C₅ Bound: Constructive Search Strategy

## Problem
Minimize max_k ∫₀² h(x)(1-h(x+k))dx subject to h:[0,2]→[0,1], ∫h=1.

## Why Gradient Descent Fails
- Many local minima in the landscape
- Narrow feasible region from ∫h=1 constraint
- Dense discretization (800 points) is too fine for global structure

## Winning Approach: Explicit Construction

### Step 1: Coarse-Grained Design
- Use num_intervals=50 to 100
- Design piecewise constant functions with few breakpoints
- Optimize breakpoint positions and block heights

### Step 2: Structural Classes to Explore
1. **Single block**: h=1 on [0,1], 0 elsewhere (baseline)
2. **Split block**: h on [0,a] and [2-a,2] for various a∈[0.2,0.8]
3. **Three-block**: h on [0,a], [b,c], [2-c,2] with different heights
4. **Symmetric wave**: h(x) = 0.5 + 0.5*sigmoid(10*(x-1)) and variants
5. **Concentrated peaks**: Narrow high-value regions separated by zeros

### Step 3: Implementation Strategy
- Replace Adam with: evolutionary search over breakpoints OR explicit enumeration
- Start with 50 intervals, find good c5_bound, then refine to 800
- Use multiple independent searches from different structural seeds
- Track best c5_bound across all searches

### Step 4: Hyperparameter Guidance
- num_intervals: 50 (coarse), then 200, then 800 (refinement)
- num_restarts: 10-20 different structural seeds
- Don't rely on learning rate tuning; focus on search diversity

## Execution Plan
1. Rewrite the optimizer to use explicit construction
2. Start with 50 intervals and 10-15 structural restarts
3. Try at least 3-4 different structural classes
4. If promising, refine to 200-800 intervals
5. Target: c5_bound < 0.38092303510845016 for combined_score > 1.0
