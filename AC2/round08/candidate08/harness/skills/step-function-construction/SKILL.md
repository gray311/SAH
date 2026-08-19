---
name: step-function-construction
description: Playbook for constructing TRUE step functions from random specs using jnp.piecewise. Never use linear ramps!
---

# Step Function Construction Playbook

## Critical: Step = Piecewise-Constant, NOT Linear

The seed program creates PIECEWISE-LINEAR functions via jnp.linspace or linear interpolation. This FAILS.

You must create PIECEWISE-CONSTANT step functions using jnp.piecewise with CONSTANT heights.

## Workflow

### Step 1: Generate Random Spec

CALL generate_step_spec FIRST to get:
- num_steps: 3-8 (more complex may achieve higher C2)
- symmetric: true/false (try both)
- boundaries: array of x-coordinates where steps occur
- heights: array of constant values for each step (0.5-2.5)

### Step 2: Convert Spec to Code

In edit_solution:

1. Create domain: x = jnp.linspace(-10, 10, num_intervals)
2. Define conditions based on boundaries
3. Use jnp.piecewise: f = jnp.piecewise(x, [cond1, cond2, ...], [h1, h2, ...])
4. h1, h2, etc. MUST be CONSTANT NUMBERS, NOT functions of x

Example for 4 steps:
```python
x = jnp.linspace(-10, 10, 400)
f = jnp.piecewise(x, 
    [x < -0.5, (x >= -0.5) & (x < 0.5), (x >= 0.5) & (x < 2.0), x >= 2.0],
    [1.2, 1.8, 2.1, 0.9])
```

### Step 3: Rewrite Objective Function

Update _objective_fn to:
- Use the NEW step function interface
- Keep the convolution and C2 calculation the same
- Ensure f_non_negative = jax.nn.relu(f)

### Step 4: Verify with analyze_step_structure

Call analyze_step_structure after edit. Verify:
- function_type: "step"
- is_piecewise_constant: True
- num_regions matches your num_steps

If wrong, RE-Evaluate the edit. Common errors:
- Used jnp.linspace instead of jnp.piecewise
- Heights are functions of x instead of constants
- Conditions are wrong (too many/few steps)

### Step 5: Probe & Evaluate

- Probe 3-5 variants to rank them cheaply
- Evaluate only TOP 1-2 (max ~5 evals total)
- If no improvement, generate NEW random spec and repeat

## Checklist

- [ ] Called generate_step_spec first
- [ ] Used jnp.piecewise with CONSTANT heights
- [ ] Verified with analyze_step_structure (is_piecewise_constant: True)
- [ ] Only then probed/evaluated
- [ ] Max 5-6 evals total to stay in budget
