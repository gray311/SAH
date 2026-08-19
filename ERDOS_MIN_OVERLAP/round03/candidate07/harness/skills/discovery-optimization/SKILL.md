---
name: discovery-optimization
description: "Discrete combinatorial search for Erd\u0151s C5 problem. Generates step function candidates\ndirectly (not via latents), uses discrete mutations, evaluates top variants only.\nAvoids gradient descent which fails on this non-differentiable objective."
---

# Erdős C5 - Discrete Step Function Search

## Problem Understanding
Find step function h: [0,2]→[0,1], ∫h=1, minimizing max_k ∫h(x)(1-h(x+k))dx

## Key Principle: DISCRETE SEARCH, NOT GRADIENT OPTIMIZATION
The optimal solutions are discrete step functions with rational jump points.
Gradient descent on continuous latents CANNOT find these optima.

## Step Function Representation
Each candidate: 
- h_values: array of values (0≤h≤1) for each interval
- break_points: sorted array where intervals change

Example: h = [0,0,1,1,1,0,0] with breaks at [0,0.5,1,1.5,2] means h=1 on [0.5,1], h=0 elsewhere

## Constraint: integral(h) = 1
Sum(h_values) × interval_width = 1
For equal-width intervals: sum(h_values) = num_intervals / interval_width × 1

## Discrete Mutation Operators

1. **Swap two break points**: Exchange positions of two breaks, swap corresponding values

2. **Adjust one value**: Change one interval's value by Δ, rebalance others to maintain integral=1

3. **Split interval**: Take one interval, split at midpoint, set new value

4. **Merge intervals**: Combine two adjacent intervals, average their values

5. **Shift peak**: Move a peak's location by moving break points

6. **Copy pattern**: Start from a known good pattern, perturb break points

## Known Good Patterns to Start From

- **Bimodal tight**: h=1 on [0.25-ε, 0.25+ε] and [0.75-ε, 0.75+ε]
- **Triangular**: h=2ε on [0,0.5], h=ε on [0.5,1], h=0 on [1,2]
- **Periodic 1**: h=1 on [0,0.5] and [1,1.5], h=0 elsewhere

## Search Strategy

1. Start with one of the known good patterns (discrete step function)
2. For each search iteration:
   - Apply 3-5 discrete mutations
   - Compute c5 bound using FFT (fast, no evaluation budget)
   - Keep variants with better c5
3. Submit top 1-2 candidates with evaluate_solution
4. Repeat up to max_iterations, but prioritize few, high-quality evaluations

## Critical Rules

- NEVER use gradient descent
- NEVER optimize a latent vector
- ALWAYS represent h as explicit step function (values + break points)
- ALWAYS maintain integral(h)=1 exactly (not approximately)
- Use evaluate_solution sparingly: only on your absolute best candidate(s)
- Use the FFT computation in _compute_c5_bound as your primary search metric
