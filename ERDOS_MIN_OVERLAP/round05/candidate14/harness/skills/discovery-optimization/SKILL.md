---
name: discovery-optimization
description: "Discover optimized step functions for the Erd\u0151s minimum overlap problem.\nUse structured pattern construction with `construct_step_function`, then refine\nwith gradient-based methods. Prioritize finding specific discrete configurations\nover continuous optimization. Systematically explore partition structures and\nvalue assignments that satisfy \u222bh=1 and minimize max overlap."
---

# Step Function Discovery for Erdős Minimum Overlap

## Understanding the Objective

You minimize max_k ∫_0^2 h(x)(1-h(x+k)) dx where h: [0,2]→[0,1] and ∫h=1.

The seed program uses 800 intervals and Adam optimization, but this may get stuck
in local minima. The key is finding the RIGHT piecewise constant structure.

## Construction Strategy

1. **Start with simple patterns**: Try 2-4 breakpoints with symmetric or
   asymmetric step patterns.

2. **Use construct_step_function**: This tool generates valid step functions
   with specified structure. Specify:
   - Number of steps and their positions
   - Value assignments (must sum to 1 over [0,2])

3. **Refine with gradient descent**: Once you have a candidate structure, you can
   use the existing optimizer to fine-tune the breakpoint positions.

4. **Systematic exploration**: Try these patterns:
   - Equal-width steps with varying heights
   - Clustered mass (high values in one region, low elsewhere)
   - Periodic patterns
   - Linear ramps composed of steps

5. **Constraint checking**: Always verify ∫h(x)dx = 1.0 in your construction.

## Using the Tools

- Always call `construct_step_function` FIRST to understand what's achievable.
- Use `probe_solution` to quickly rank multiple construction candidates.
- Only call `evaluate_solution` on your best 1-2 candidates.
- When `combined_score > 1.0`, you've found a new bound - stop and finish.
- If stuck after 10 evaluations, try a fundamentally different construction
  strategy (not just parameter tuning).

## Example Construction

A simple valid h: h(x) = 0.5 for x ∈ [0,2] gives ∫h=1.0.
The correlation would be ∫0.5×0.5 = 0.25 everywhere, so max = 0.25.

Better: asymmetric step function with more mass concentrated where overlaps
are less severe.

Remember: The goal is a SPECIFIC step function, not "optimizing parameters" of a
continuous function. Use constructive design!
