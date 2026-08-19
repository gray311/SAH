---
name: discovery-optimization
description: "Construction-based search for Erdos minimum overlap"
---

# Construction-Based Search for Erdos Minimum Overlap

## Core Idea
Instead of optimizing in continuous latent space, explicitly CONSTRUCT step functions
by specifying their piecewise structure. This gives you DIRECT CONTROL over the solution.

## Step Function Construction Pattern

A step function h: [0, 2] -> [0, 1] is defined by:
1. Partition [0, 2] into n intervals: [x0, x1), [x1, x2), ..., [xn-1, 2]
2. Assign a value h_i in [0, 1] to each interval
3. Constraint: sum(h_i * (x_{i+1} - x_i)) = 1 (integral constraint)

## Search Strategy

### Phase 1: Simple Constructions (2-5 intervals)
- Uniform: n intervals, all h_i = 1/n (satisfies integral constraint automatically)
- Concentrated: One interval with h=1, rest with h=0 (edge case)
- Alternating: Values a, b alternating where a * width_a + b * width_b = 1

### Phase 2: Systematic Grid Search
For fixed n intervals:
1. Choose n-1 boundary points in (0, 2), sorted
2. Choose n-1 values in (0, 1), then solve for last value to satisfy integral
3. Compute C5 bound and score

### Phase 3: Value Optimization
Once boundaries are fixed, use simple gradient-based optimization on the VALUES only.
This is much more tractable than optimizing both boundaries and values.

## Key Insight
The optimal solution might be a VERY SIMPLE step function (2-4 intervals) that the
continuous optimizer never finds because it gets stuck in a complex latent space optimum.

## Implementation Template
Edit EVOLVE-BLOCK to implement:
```python
def construct_step_function(n_intervals, boundaries, values):
    # boundaries: n-1 points in (0, 2)
    # values: n values in [0, 1]
    # Returns h as numpy array of length n_intervals (or padded)
    h = np.zeros(n_intervals)
    for i in range(n_intervals):
        h[i] = values[i]
    return h
```
