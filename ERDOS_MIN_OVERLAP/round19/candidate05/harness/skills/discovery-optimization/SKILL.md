---
name: discovery-optimization
description: "Edit the seed optimizer's _get_best_initialization method to add new pattern variations. Each pattern is trained for 59000 steps."
---

# Strategy: Edit _get_best_initialization to Add New Patterns

## Why Edit, Not Generate?

The seed optimizer has a fixed _get_best_initialization method that generates initializations and trains each for 59000 steps.
You cannot "generate candidates" separately - you must EDIT THIS CODE to add new patterns it can train.

## Pattern Categories to Insert

1. **Concentrated Peaks**: Place most probability mass at a single narrow region
   - h(x) ~ 1 for x in [c-0.1, c+0.1], ~0 elsewhere
   - Try centers at: 0.1, 0.5, 0.9, 1.2, 1.6, 1.9

2. **Asymmetric Step Functions**: 
   - High on [0, 0.33], low on [0.67, 2] (integral constraint: area ~1)

3. **Sinusoidal Variants**: sin(pi*x), sin(2*pi*x) with different phases

## Editing Technique

1. Find the existing pattern block in _get_best_initialization
2. Add a new pattern block after the last existing pattern
3. Each pattern must use jax.lax.stop_gradient, sigmoid, and compute c5 bound
4. Call edit_solution with the new code

## Evaluation Strategy

1. Edit to add 1 new pattern per iteration
2. Run edit_solution to apply the edit
3. Call evaluate_solution once (the optimizer will try all patterns)
4. If combined_score improves (>1.0), try similar patterns
5. With 30 evals, you can test ~15 new patterns

## Concrete Pattern Example

# Pattern 15: Concentrated peak at 0.25
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

## Try Different Centers

Change c to: 0.25, 0.5, 0.75, 1.25, 1.5, 1.75
