---
name: discovery-optimization
description: "C\u2085 optimizer using discrete piecewise construction. Builds explicit step functions with controlled breakpoints, bypassing failed gradient search."
---

# Erdős C₅ Bound - Piecewise Construction Strategy

## Why Gradient Descent Fails

- 800-dimensional sigmoid space has pathological landscape
- Integral constraint ∫h=1 is numerically unstable with penalty
- Optimal h is piecewise constant, not smooth sigmoid

## Construction Strategy

### Step 1: Define Breakpoints

Try these configurations:

**Single interval**: h = 0.5 on [0,2]
**Two intervals**: h = a on [0,t], h = b on [t,2] with a*t + b*(2-t) = 1
**Three intervals** (most promising): h = [h1, h2, h3] on [0,t1], [t1,t2], [t2,2]
with constraint h1*t1 + h2*(t2-t1) + h3*(2-t2) = 1

Try symmetric patterns: [1, 0, 1] or [0, 0.5, 1]

### Step 2: Evaluate Each Candidate

For each constructed h:
1. Verify h ∈ [0,1] everywhere
2. Verify ∫h = 1 (within tolerance)
3. Compute c5_bound via the optimizer's _compute_c5_bound method
4. Compute combined_score = 0.38092303510845016 / c5_bound

### Step 3: Search Over Configurations

Systematically try:
- Different numbers of intervals: 2, 3, 4, 5
- Different breakpoint patterns (equal spacing, concentrated, symmetric)
- Different height assignments (monotonic, bipartite, uniform)

### Step 4: Example Candidates

1. **Uniform**: h = 0.5 on [0,2]
2. **Left-heavy**: h = 1 on [0,1], h = 0 on [1,2]
3. **Bimodal**: h = 0.5 on [0,0.5] ∪ [1.5,2], h = 0 elsewhere
4. **Trinomial**: h = [1, 0, 1] on [0,2/3], [2/3,4/3], [4/3,2] normalized

## Key Insight

The mathematical constant C₅ comes from harmonic analysis theory. Extremal functions are often simple piecewise constants. Build them directly!
