---
name: discovery-optimization
description: "Optimize step functions for C\u2082 inequality. Use probes to test parameter changes (width, height, position), then confirm improvements with full evaluation."
---

# C₂ Step Function Optimization

Goal: Beat current best score of 1.03431 by improving step function parameters.

## Search Strategy
1. **Start with probes**: Test small parameter changes (±10% width/height adjustments, ±5% position shifts)
2. **Track best**: Keep parameters from highest probe score
3. **Confirm with eval**: Only call evaluate_solution when probe suggests potential improvement
4. **Iterate**: If eval improves, build on it; if not, try different mutations

## Parameter Mutations to Try
- Step height: ±0.05 to ±0.2 (seed uses heights like 1.42, 1.92, 1.62, etc.)
- Step width: ±5% of current width
- Step position: ±3% of domain
- Number of steps: Try 300-500 intervals
- Pattern variants: Asymmetric peaks, multi-peak, plateau variants

## When to Probe
- At each iteration, before full evaluation
- Test 3-5 variants with different parameters
- Pick best for final evaluation

## When to Evaluate
- When probe scores are consistently higher than best_so_far
- When you have a coherent parameter set to test
- Fewer than 15 evals remaining

## Recovery
- If eval score drops, revert to previous best parameters
- If no improvement after 5 iterations, try fundamentally different pattern class
- Budget ending: make only one more targeted edit before finishing
