---
name: pattern-edit-strategy
description: Edit the seed optimizer's _get_best_initialization to add new pattern variations. Focus on concentrated peaks at different centers.
---

# Pattern Edit Strategy for Erdos Optimization

## Understanding the Problem

The seed optimizer's _get_best_initialization method already has 15 patterns.
Each pattern is trained for 59000 steps. The best result across all patterns is returned.

To improve, you must ADD new patterns that the optimizer can evaluate.

## Why Edit, Not Generate?

- The optimizer trains each pattern for 59000 steps
- You cannot "generate candidates" separately
- You must EDIT the code to add new patterns

## Best Pattern Type: Concentrated Peaks

Place most probability mass at a single narrow region.
Try centers at: 0.25, 0.5, 0.75, 1.25, 1.5, 1.75

## Editing Process

1. Call generate_pattern_edit with pattern_type="concentrated_peak" and a center value
2. The tool returns a code snippet
3. Insert the pattern block into _get_best_initialization (after Pattern 14)
4. Call edit_solution to apply the edit
5. Call evaluate_solution (tests all patterns)
6. If combined_score > 1.0, try similar patterns with different centers

## Example

Add this new pattern:

# Pattern 15: concentrated_peak at 0.25
key, subkey = jax.random.split(key)
x = jnp.linspace(0, 2, N)
c = 0.25
latent = jnp.zeros(N)
mask = jnp.abs(x - c) < 0.12
latent = latent.at[mask].set(6.0)
latent = latent.at[~mask].set(-6.0)
latent = latent + jax.random.normal(subkey, (N,)) * 0.3
latent = jax.lax.stop_gradient(latent)
h = jax.nn.sigmoid(latent)
j_val = 1.0 - h
h_padded = jnp.pad(h, (0, N))
j_padded = jnp.pad(j_val, (0, N))
corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
correlation = jnp.fft.ifft(corr_fft).real
obj = jnp.max(correlation * self.dx)
if obj < best_obj:
    best_obj = obj
    best_latent = latent

## Budget Management

- 30 total evals
- 1 eval per edit->evaluate cycle
- Test ~15 new patterns
