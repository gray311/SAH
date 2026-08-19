---
name: step-function-construction
description: Explicitly construct step functions by specifying intervals and values, then compute C5 bound directly.
---

# Step Function Construction Strategy

## Why Construction > Optimization

The seed optimizer tries 12 initialization patterns but OPTIMIZES in continuous space.
This means it can NEVER find a solution that lies exactly on a simple step function boundary.

By explicitly CONSTRUCTING step functions, you:
1. Have EXACT control over the piecewise structure
2. Can systematically search the finite space of simple constructions
3. Avoid getting stuck in complex latent space local optima

## Construction Algorithm

### Step 1: Define Intervals
Choose n boundaries: 0 = x0 < x1 < ... < xn = 2

### Step 2: Assign Values
Choose values v1, v2, ..., vn where each vi in [0, 1]

### Step 3: Enforce Integral Constraint
sum(vi * (xi - x_{i-1})) = 1

### Step 4: Compute C5 Bound
h_padded = pad(h, N)
j_padded = 1 - h_padded
corr = FFT(h_padded) * conj(FFT(j_padded))
correlation = IFFT(corr).real
C5 = max(correlation * dx)

## Search Patterns

### Pattern A: Uniform partitions
n intervals, boundaries = linspace(0, 2, n+1), values = [1/n] * n

### Pattern B: Two-interval split
One boundary at x, values = [a, b] where a*x + b*(2-x) = 1

### Pattern C: Concentrated mass
One narrow interval with value ~1, rest with value 0

### Pattern D: Golomb-like spacing
Use optimal spacing patterns from combinatorial design theory
