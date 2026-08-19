---
name: discretization-guide
description: Playbook for numerical optimization and discretization choices in C2 maximization. Focus on resolution, stability, and function diversity.
---

# Discretization and Numerical Optimization Guide

## Understanding the Trade-offs

Discretization resolution (num_intervals) affects:
- **Accuracy**: More intervals = more accurate convolution via FFT
- **Speed**: O(n log n) but constant factor grows with n
- **Local minima**: Coarse discretization traps optimization in suboptimal solutions

## Guidelines by Strategy

### Simple Step Functions
- 400-600 intervals sufficient
- Focus on pattern diversity, not resolution

### Complex Piecewise Functions
- 800-1000 intervals recommended
- Each region needs adequate sampling

### Continuous/Differentiable Functions
- 1200+ intervals for accurate derivatives
- Consider analytic solutions where possible

### Multi-scale Approach
1. Start: 200-400 intervals, many iterations
2. Transition: 600-800 intervals
3. Refine: 1000-1600 intervals, local search

## Stability Checklist

- [ ] FFT padding: pad to 2× natural size before FFT
- [ ] Non-negativity: f(x) >= 0 (use softmax, exp, or abs+epsilon)
- [ ] Normalization: scale so ∫f = 1 for fair C2 comparison
- [ ] Boundary handling: convolution boundary artifacts
- [ ] Numerical precision: use jnp.float64 for critical computations

## Common Errors to Avoid

- Using 200 intervals for complex functions (inaccurate)
- Forgetting FFT padding (boundary artifacts)
- Not normalizing (scaling effects on C2)
- Staying too long on coarse discretization (local minima)

## When to Call analyze_discretization_quality

- Before every major edit
- When probes show unexpected behavior
- When switching function representations
- To decide next resolution level in multi-scale approach
