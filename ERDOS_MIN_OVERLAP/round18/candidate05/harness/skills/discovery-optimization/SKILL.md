---
name: discovery-optimization
description: "Code editing for Erdos optimization: edit hyperparameters and initialization patterns in the seed optimizer. The seed has a sophisticated 59k-step optimizer - modify it to find better solutions, don't rely on static candidate generation."
---

# Erdos Optimization via Code Editing

## The Seed Optimizer Structure

- Hyperparameters class: num_intervals (800), num_steps (100000), penalty_strength (60), num_restarts (3)
- _get_best_initialization(seed): generates 15 patterns via jax.random
- _compute_c5_bound(h): FFT-based analytical c5 computation (fast!)

## Editing Strategy

### Phase 1: Hyperparameter Sweep (1 eval per candidate)
Test ONE change at a time:

# Increase resolution
num_intervals = 1000 or 1200

# More training
num_steps = 80000 or 100000 or 150000

# Stronger penalty for integral constraint
penalty_strength = 80 or 100 or 150

# More restarts for better local optima search
num_restarts = 5 or 8 or 10

### Phase 2: Add New Initialization Patterns

Add to the FOR pattern in range(15):

# Pattern 16: Dense Golomb (5 optimal marks)
marks = jnp.array([0.0, 0.33, 0.66, 1.33, 1.66])
latent = jnp.zeros(N)
for m in marks:
    mask = jnp.abs(x - m) < 0.12
    latent = latent.at[mask].set(6.0)
latent = latent - 3.0

# Pattern 17: Two separated blobs
latent = jnp.zeros(N)
latent[:int(N*0.6)] += 5.0
latent[int(N*0.75):] += 5.0

# Pattern 18: Four narrow peaks
for center in [0.25, 0.75, 1.25, 1.75]:
    mask = jnp.abs(x - center) < 0.1
    latent = latent.at[mask].set(7.0)
latent = latent - 4.0

### Phase 3: Latent Amplification

Before the existing loop, add:
scale = 2.0  # or 2.5, or 3.0
key = jax.random.PRNGKey(seed)
latent = jax.random.normal(key, (N,)) * scale

## Workflow

1. Start with num_intervals=1000, num_steps=80000, penalty_strength=100, num_restarts=5

2. If stuck after 3 edits, add pattern 16 (dense Golomb)

3. If still stuck, add pattern 17 or 18

4. Finally, try latent amplification (scale=2.0)

## Expected Outcome
Better hyperparameters or patterns enable the 59k-step optimizer to find h with c5_bound < 0.37, giving combined_score > 1.0.
