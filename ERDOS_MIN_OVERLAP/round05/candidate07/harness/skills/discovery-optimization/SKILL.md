---
name: discovery-optimization
description: "Optimize Erd\u0151s C5 bound by: (1) adding deterministic multi-scale initialization patterns, (2) enforcing integral=1 constraint exactly before optimization, (3) early-stopping runs that plateau. Use probe to rank initializations cheaply. Goal: beat C5 \u2264 0.38092303510845016."
---

# Erdős C5 Optimization Strategy

## Goal
Maximize combined_score = 0.38092303510845016 / c5_bound. Target: c5_bound < 0.380923 to get score > 1.

## Problem
Minimize: max_k ∫₀² h(x)(1-h(x+k)) dx
where h: [0,2] → [0,1] and ∫₀² h(x) dx = 1 exactly.

## Three-Stage Protocol

### Stage 1: Enhanced Initialization
**Preserve the seed's 12 patterns EXACTLY. Do not modify them.**

Add 4 new deterministic patterns after the seed's 12:

```python
# Pattern 12: Symmetric block (h concentrated in [0.5, 1.5])
x = jnp.linspace(0, 2, N)
latent = jnp.where((x >= 0.5) & (x < 1.5), 10.0, -10.0)

# Pattern 13: Two-block equal (h concentrated in [0,0.5] and [1.5,2])
latent = jnp.where((x < 0.5) | (x >= 1.5), 10.0, -10.0)

# Pattern 14: Three-block (1:2:1 ratio)
latent = jnp.where((x < 0.5) | (x >= 1.5), 8.0, jnp.where((x >= 0.5) & (x < 1.5), -8.0, 0.0))

# Pattern 15: Scaled sawtooth (smooth transition)
x = jnp.linspace(0, 2, N)
latent = 4.0 * jnp.sin(jnp.pi * x) + 2.0
```

Key: Use large amplitudes (±8 to ±10) before sigmoid to ensure sharp step functions. The sigmoid will squash them to [0,1] while preserving the step structure.

### Stage 2: Constraint Validation Gate
**After selecting the best latent across all patterns, BEFORE optimizing, add:**

```python
# Validate integral constraint
integral_h = jnp.sum(h) * self.dx
constraint_violation = jnp.abs(integral_h - 1.0)
if constraint_violation > 1e-6:
    # Scale h to satisfy integral=1 exactly
    scale_factor = 1.0 / integral_h
    h = h * scale_factor
    # Clamp to [0,1]
h = jnp.clip(h, 0.0, 1.0)
```

Place this right after the `_get_best_initialization` returns, before any optimization. This ensures every restart starts from a feasible point.

### Stage 3: Early Stopping with Best Tracking
**Modify `_optimize_single_run` to include:**

```python
best_c5_in_run = jnp.inf
plateau_counter = 0
patience = 5000  # steps without improvement triggers early stop

for step in range(self.hypers.num_steps):
    latent_h_values, opt_state, loss = train_step(latent_h_values, opt_state)
    
    # Track best C5 (objective without penalty)
    c5_no_penalty = self._compute_c5_bound(latent_h_values)
    if c5_no_penalty < best_c5_in_run:
        best_c5_in_run = c5_no_penalty
        plateau_counter = 0
    else:
        plateau_counter += 1
    
    # Early stop if plateaued
    if plateau_counter >= patience:
        break
```

This prevents wasting 59k steps on a bad restart. If progress stalls, abandon and try a new seed.

## Probe Strategy
Before full optimization of a new restart pattern:
1. Call `probe_solution` on the raw h (before optimization)
2. Check if probe C5 < 0.35 (promising threshold)
3. If yes, invest full optimization. If no, skip.

This filters out unpromising patterns cheaply.

## Editing Discipline
- ONE edit per turn. Use SEARCH/REPLACE to add patterns after pattern 11.
- Add constraint validation after `_get_best_initialization`.
- Add early stopping logic inside `_optimize_single_run`.
- Evaluate after each stage completes.

## Final checklist
- [ ] 16 patterns total (12 original + 4 new)
- [ ] Constraint validation with scaling
- [ ] Early stopping with plateau detection
- [ ] Best C5 tracked across restarts
- [ ] Probe used to filter unpromising restarts
