---
name: step-function-constructions
description: Expert methods for constructing step functions to minimize Erdős overlap. Use explicit piecewise definitions, not gradient optimization.
---

# Step Function Constructions for Erdős C5 Bound

## Why Gradient Descent Fails
The objective max_k ∫h(x)(1-h(x+k))dx has many local optima. 
Gradient descent from random starts gets trapped. We need explicit constructions.

## Construction Strategies

### 1. Single Block (Baseline)
h = 2.0 on [0, 0.5], h = 0 elsewhere
- Integral: 1.0 ✓
- This is a natural starting point

### 2. Two Equal Blocks
h = c on [0.25, 0.75], h = 0 elsewhere
- Integral: c * 0.5 = 1.0 ⇒ c = 2.0
- More spread out than single block

### 3. Symmetric Three-Block
h = a on [0, a] ∪ [1-a, 1], h = b on [a, 1-a]
- Integral: 2*a*a + b*(1-2*a) = 1.0
- Choose a, then solve for b: b = (1 - 2*a²)/(1-2*a)
- Try a = 0.1, 0.2, 0.25, etc.

### 4. Concentrated Mass
h = 4.0 on [0, 0.25], h = 0 elsewhere
- Integral: 1.0 ✓
- Very concentrated, high peaks

### 5. Multi-Scale Construction
Start with base pattern, add smaller features
- h = 2.0 on [0, 0.5] (base)
- Add h = c on [0.1, 0.2] with negative contribution elsewhere
- This is complex; start simple first

### 6. Uniform Distribution (Upper Bound Check)
h = 0.5 everywhere on [0, 2]
- Integral: 1.0 ✓
- Compute c5_bound to establish baseline

## Algorithm
For each construction:
1. Define breakpoints and raw values
2. Compute integral, scale to make ∫h=1
3. Verify 0 ≤ h ≤ 1 after scaling (some constructions violate this!)
4. Compute c5_bound using FFT-based convolution
5. Track the best c5_bound found

## Key Insight
The optimal solution likely has a specific symmetric structure related to 
the Fourier transform properties of the autocorrelation. Explore symmetric patterns first.
