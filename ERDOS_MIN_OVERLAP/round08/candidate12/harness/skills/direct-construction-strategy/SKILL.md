---
name: direct-construction-strategy
description: Systematic construction of candidate step functions for the Erdős C₅ problem. Bypasses gradient descent by directly building solutions with known structures.
---

# Direct Construction Strategy for Erdős C₅ Problem

## Why Direct Construction Works

The gradient-based optimizer gets stuck in local optima. Instead, construct
candidate solutions with specific mathematical properties that are known to
perform well for overlap minimization.

## Pattern Library

### 1. Single Step
- h(x) = 1 for x ∈ [0,1], 0 elsewhere
- Integral = 1 ✓
- Simple baseline, often good starting point

### 2. Double Step
- h(x) = 1 for x ∈ [0,0.5] ∪ [1.5,2], 0 elsewhere
- Integral = 1 ✓
- Spreads mass to reduce overlap

### 3. Symmetric Multi-Step
- Divide [0,2] into k equal intervals, put h=1/k on each
- Exploits symmetry to minimize correlation

### 4. Concentrated Mass
- h(x) = 1 for x ∈ [0.5,1.5], 0 elsewhere
- Integral = 1 ✓

### 5. Triangular Wave
- h(x) = 1 - |x-1| for x ∈ [0,2]
- Smooth, symmetric, integral = 1 ✓

### 6. Sine Wave
- h(x) = 0.5 + 0.5*sin(π*x) for x ∈ [0,2]
- Smooth oscillation, integral = 1 ✓

## Search Procedure

1. Start with coarse discretization (N=100-200)
2. Try each pattern in the library
3. Record the best c5_bound for each pattern
4. Refine promising patterns with finer discretization (N=500-1000)
5. For very promising candidates, use local search to tweak parameters
6. Evaluate final candidates with full evaluation

## Key Insight

The optimal h likely has a **piecewise constant** structure with few breakpoints.
Gradient descent from random starts struggles to find this. Direct construction
systematically explores this structured space.
