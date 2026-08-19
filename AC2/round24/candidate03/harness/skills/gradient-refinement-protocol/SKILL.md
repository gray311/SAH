---
name: gradient-refinement-protocol
description: Step-function refinement using parameter extraction, targeted mutations, and JAX gradient ascent. Avoid random family jumps.
---

# Gradient Refinement Protocol for Step Functions

## Phase 1: Parameter-Extracted Mutations (iterations 1-15)

1. Call analyze_step_parameters to get boundaries, heights, peak info
2. Generate 3 targeted mutations:
   - Mutation A: Widen highest peak by 5% (expand start/end indices)
   - Mutation B: Redistribute heights (tallest +0.1, shortest -0.1)
   - Mutation C: Shift peak by 5% of domain (adjust start indices)
3. Probe all 3, evaluate best
4. If no improvement: try opposite direction for Mutation A

## Phase 2: JAX Gradient Ascent (iterations 16-25)

1. Use @jax.grad on -c2_ratio to get gradients w.r.t. each parameter
2. Take step: new_param = param + 0.05 * gradient
3. Clip to valid range (heights > 0, indices in [0, num_intervals])
4. Probe 2 variants (ascent and descent), evaluate best
5. If gradient norm < 0.001: switch to Phase 3

## Phase 3: Strategic Reinitialization (iterations 26-30)

1. Keep highest peak height and position
2. Reinitialize 70% of parameters with std=0.1*value
3. Try 2 variants: (a) keep peak, randomize others; (b) split peak
4. Probe, evaluate best, submit if c2 > 0.8962799441554086

## Key Rule
NO random generation - always refine existing parameters with gradients or small perturbations.
