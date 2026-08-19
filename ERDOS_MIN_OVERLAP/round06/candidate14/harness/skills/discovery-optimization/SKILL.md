---
name: discovery-optimization
description: "Erdos C5 optimization harness. Focus on direct piecewise constructions. Use probe_solution for rapid variant ranking. Target combined_score > 1.0."
---

# Erdos C5 Bound Optimization

## The Mathematical Problem

Minimize: max_k integral_0^2 h(x)(1-h(x+k))dx

Subject to: h:[0,2]->[0,1], integral_0^2 h(x)dx = 1

Current best: 0.38092303510845016 (combined_score = 1.0)

## Why Gradient-Based Optimization Fails

The seed's Adam optimizer is stuck because:
- 800-interval discretization creates high-dimensional landscape
- Random initializations miss global structure
- Gradient descent gets stuck in symmetric solutions

## Recommended Approaches

### Approach A: Direct Piecewise Construction

Replace the optimizer with direct construction of h:

```python
n = 800
h = jnp.zeros(n)
break1 = int(0.5 * n)
h = h.at[:break1].set(0.5)
```

Then optimize only the breakpoint positions.

### Approach B: Strategic Initializations

Replace seed's 12 patterns with mathematically motivated ones:

1. Single step: h=1 on [0,1], h=0 elsewhere
2. Double step: h=0.5 on [0,0.5] union [1.5,2]
3. Three-step symmetric: h=1/3 on [0,1/3], [2/3,1], [4/3,2]
4. Concentrated: h=1 on [0,0.5], h=0 elsewhere

### Approach C: Coarse-to-Fine Optimization

Phase 1: num_intervals=50, num_steps=5000
Phase 2: num_intervals=200, resume with best h, num_steps=10000
Phase 3: num_intervals=800, resume, num_steps=20000

## Execution Protocol

1. Analyze: Use probe_solution to quickly score 3-5 candidate edits
2. Construct: Make a complete rewrite of the EVOLVE-BLOCK
3. Evaluate: Spend one full evaluate on the best probed variant
4. Iterate: If no progress after 2-3 iterations, try a completely different approach

## Tool Usage

- probe_solution: Rank candidate edits (FREE, fast)
- evaluate_solution: Confirm promising variants (consumes main budget)
- edit_solution: For direct construction, do complete rewrites

## Success Criteria

- combined_score > 1.0 is a breakthrough
- combined_score approx 0.999641 means you're still in the same basin
- Try 8-10 iterations max, explore diverse strategies
