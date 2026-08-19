---
name: true-step-function-creation
description: Playbook for creating TRUE piecewise-constant step functions using step_config_generator. Step functions must be CONSTANT over intervals, not linear ramps.
---

# Creating TRUE Step Functions for C2 Maximization

## Critical: Step vs Linear

The seed program uses piecewise-LINEAR optimization. Step functions must be PIECEWISE-CONSTANT (flat over intervals, not sloped).

## Using step_config_generator

1. CALL step_config_generator FIRST to get structured parameters
2. Extract intervals: list of (start, end, height) tuples
3. Create function with jnp.piecewise or jnp.where:
   - jnp.piecewise(x, [conditions], [values])
   - Or chain jnp.where for simpler cases
4. Ensure function is CONSTANT over each interval (no linear ramps)

## Example Edit from step_config_generator Output

If step_config_generator returns:
  intervals: [(-0.4, -0.2, 0.7), (-0.2, 0.2, 1.3), (0.2, 0.4, 0.7)]

Edit to create:
  def create_step_function(x, intervals):
      # Piecewise-constant function
      f = jnp.zeros_like(x)
      for (start, end, height) in intervals:
          mask = (x > start) & (x < end)
          f = f.at[mask].set(height)
      return f

Or using jnp.piecewise:
  conditions = [(x > start_1) & (x < end_1), (x > start_2) & (x < end_2), ...]
  values = [h1, h2, h3, 0.0]  # 0 outside intervals
  f = jnp.piecewise(x, conditions, values)

## Probe-Before-Eval Protocol

1. Get 3-5 configurations from step_config_generator
2. Create step functions, probe each
3. Rank by probe score
4. Evaluate top 2 only (max 4 evals total)

## Common Mistakes to Avoid

- Using linear interpolation instead of constant values
- Not using step_config_generator (random perturbations don't work)
- Evaluating before probing (wastes precious evals)
- Creating too many evals (max ~4, use probes for ranking)
