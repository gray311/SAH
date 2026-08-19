---
name: step-function-strategy
description: Design step functions with piecewise constant structure for Erdős problem.
---

# Step Function Strategy for Erdős Min Overlap

## Critical Insight
The seed optimizer uses sigmoid(latent) which produces SMOOTH functions. The Erdős problem needs TRUE STEP FUNCTIONS (piecewise constant) for optimal solutions.

## Two-Phase Approach

### Phase 1: Discover Structure (Coarse Search)
- Set num_intervals = 50-100 (start coarse)
- Use num_steps = 5000 (fast exploration)
- Try penalty_strength in [3, 10, 30]
- Goal: Find which step heights and locations give low overlap

### Phase 2: Refine Structure (Fine Search)
- Increase num_intervals to 200-400
- Add more restarts for each structure
- Fine-tune step heights

## How to Edit for Step Functions

### Option A: Direct Step Latent
Change _get_best_initialization:
latent = jnp.zeros(N)
for i in range(0, N, int(N/5)):  # 5 steps
    latent[i:i+int(N/5)] = -2.0 + rng.uniform(-0.5, 0.5)
return latent  # Pass through tanh or clip, not sigmoid

### Option B: Tanh Activation
Change activation in _objective_fn:
h = jax.nn.tanh(latent_h_values) / 2.0 + 0.5  # Maps to [0,1]

### Option C: Piecewise Constant Initialization
def _get_best_initialization(seed):
    N = self.hypers.num_intervals
    x = jnp.linspace(0, 2, N)
    # Try different step configurations
    patterns = [
        jnp.where(x < 0.5, -3.0, jnp.where(x < 1.5, 2.0, -1.5)),
        jnp.where(x < 0.4, 2.0, jnp.where(x < 1.2, -1.0, 1.5)),
        jnp.where((x >= 0.2) & (x < 0.8), 1.0, jnp.where((x >= 0.8) & (x < 1.8), -0.5, 1.5)),
    ]
    best = None
    best_score = jnp.inf
    for pattern in patterns:
        h = jax.nn.sigmoid(pattern)  # Or remove sigmoid entirely
        j = 1.0 - h
        c5 = jnp.max(jnp.fft.ifft(jnp.fft.fft(h) * jnp.conj(jnp.fft.fft(j))).real)
        if c5 < best_score:
            best_score = c5
            best = pattern
    return best

## Parameter Space to Explore
- num_intervals: [50, 100, 200, 400, 800]
- num_restarts: [1, 3, 5, 10]
- num_steps: [2000, 5000, 10000, 20000, 59000]
- penalty_strength: [3, 10, 30, 100, 300]
- activation: [sigmoid, tanh/2+0.5, clip(-0.5, 1.5)]
