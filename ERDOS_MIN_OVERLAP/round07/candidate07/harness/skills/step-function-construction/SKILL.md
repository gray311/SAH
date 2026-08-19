---
name: step-function-construction
description: Expert technique - Build explicit step functions directly, abandon gradient-based optimization. Call this skill when designing candidate solutions for C₅ bound.
---

# Step-Function Construction for C₅ Bound

## Core Principle

The optimal h is likely a SIMPLE step function (2-5 intervals), NOT a complex learned function.
Gradient descent fails because:
1. The landscape is discrete/flat
2. Sigmoid transformation adds unnecessary complexity
3. We're looking for specific combinatorial structures, not smooth functions

## Construction Checklist

1. **Choose discretization**: 20-50 intervals is sufficient (not 800)
2. **Select pattern type**:
   - single_block: One interval of h=1, width=1
   - double_step: Two intervals of h=0.5, total width=1
   - boundary_mass: Mass at both ends [0,0.5] ∪ [1.5,2]
   - shifted_block: Block shifted from [0,1] to avoid self-overlap
   - three_interval: Three consecutive intervals

3. **Verify constraints analytically**:
   - Check: sum(h) × dx = 1.0 exactly (not approximately)
   - Check: all h[i] ∈ [0,1] (use 0.5 or 1.0, not arbitrary floats)

4. **Try multiple patterns**: Generate 10-20 variants with different configs

5. **Use probes to rank**: Call probe_solution 10-20 times on different patterns

6. **Full eval on top 2-3**: Only call evaluate_solution on your best candidates

7. **If stuck, radically change**: Different number of intervals, different pattern type

## Example Code Structure

```python
def build_h(pattern, num_intervals=50):
    dx = 2.0 / num_intervals
    h = jnp.zeros(num_intervals)
    
    if pattern == "boundary_mass":
        # h=1 on [0,0.5] ∪ [1.5, 2]
        h = jnp.zeros(num_intervals)
        h = h.at[:25].set(1.0)
        h = h.at[75:].set(1.0)
        # Verify integral
        
    return h
```

## Key Insight

Don't optimize h values. BUILD them explicitly based on mathematical intuition.
Try 20 different patterns, pick the best, and evaluate that.

## What to Avoid

- NO gradient descent (Adam, SGD, etc.)
- NO sigmoid transformations (use step functions directly)
- NO high discretization (20-50 intervals is enough)
- NO random noise added to latent vectors
- DO verify constraints BEFORE evaluation
- DO call probes to rank candidates before full evals
