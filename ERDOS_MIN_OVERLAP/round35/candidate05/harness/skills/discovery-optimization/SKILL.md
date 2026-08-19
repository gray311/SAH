---
name: discovery-optimization
description: "Generate diverse step-function initializations (narrow peaks, sparse distributions, multi-modal) with varied hyperparameters, then use probe_solution for screening and evaluate_solution for promising candidates."
---

# Step-Function Initialization Strategy for C5 Optimization

## Problem Understanding
The C5 bound is computed as max_k ∫ h(x)(1-h(x+k)) dx. For step functions h: [0,2]→[0,1] with ∫h=1, we want to minimize overlap between h and its shifted versions. Smooth sigmoid functions concentrate mass too diffusely; NARROW PEAKS create better separation.

## Initialization Strategy

### Step 1: Generate Diverse Structural Priors

Create 3-5 initializations with DIFFERENT structural patterns:

**Pattern A: Sparse Gaussian Peaks**
- Create 3-5 narrow Gaussian peaks (σ=0.05-0.1)
- Separate peaks by at least 0.3 units
- Scale heights to satisfy integral constraint
- Apply sigmoid to latent

**Pattern B: Multi-Step Threshold**
- Use multiple threshold points (e.g., 5-7 thresholds)
- Create piecewise constant h(x) with steps at 0.1-0.2 intervals
- Assign heights from {0, 0.2, 0.4, 0.6, 0.8, 1.0}
- Ensure integral=1

**Pattern C: Golomb-Ruler Inspired**
- Place narrow peaks at positions that minimize pairwise overlaps
- For domain [0,2], try positions like [0.2, 0.6, 1.0, 1.4, 1.8]
- Each peak has width 0.1, height scaled to integrate to 1

**Pattern D: Bipartite with Offset**
- h(x) = 1 for x ∈ [a, a+1], 0 elsewhere, shifted by a
- Vary a ∈ {0.0, 0.2, 0.4, 0.6, 0.8}
- This gives C5 ≈ 0.5, but combined with optimization may improve

**Pattern E: Random Sparse**
- Generate h with exactly K=3-7 intervals where h > 0.1
- Set random heights in [0.1, 1.0]
- Normalize to integral=1

### Step 2: Hyperparameter Exploration

For each structural pattern, try MULTIPLE hyperparameter combinations:

| num_intervals | penalty_strength | num_steps |
|--------------|------------------|----------|
| 400          | 30               | 20000    |
| 400          | 100              | 50000    |
| 800          | 60               | 30000    |
| 1600         | 200              | 100000   |

### Step 3: Use Tools Strategically

1. Generate 3-5 different initializations using the patterns above
2. Call probe_solution on each to get approximate c5_bound
3. Keep candidates with c5_bound < 0.380 (cheaper than full eval)
4. Call evaluate_solution on top 2-3 candidates
5. If any combined_score > 1.0, finish
6. If no success after 2 evals, generate NEW structural priors (e.g., if peaks were too narrow, try wider)

## Key Principles
- DIVERSITY: Different structural priors > random hyperparameter tuning
- SPARSITY: Narrow peaks, sparse intervals > smooth functions
- CONSTRAINT: Always ensure integral(h)=1 and h∈[0,1]
- ITERATE: If stuck, try fundamentally different structural patterns
- PROBE FIRST: Use probe_solution to screen before wasting evaluations

## Edit Instructions

When editing, focus on:
1. **Latent pattern**: Replace smooth latent (normal distribution) with sparse/peaked patterns
2. **Hyperparameters**: Systematically vary num_intervals, penalty_strength, num_steps
3. **Sigmoid scaling**: Adjust latent scale to get desired h(x) heights
4. **Separation**: Ensure peaks/intervals are well-separated (≥0.3 units)

## Example Edit Pattern

Instead of:
```python
latent = jax.random.normal(subkey, (N,))
```

Use:
```python
# Pattern: 3 narrow Gaussian peaks
peaks = jnp.array([0.2, 1.0, 1.8])  # positions
width = 0.08  # narrow width
h_vals = jnp.zeros(N)
for p in peaks:
    h_vals = h_vals + jnp.exp(-((x - p) / width)**2)
h_vals = h_vals / jnp.sum(h_vals * dx)  # normalize to integral=1
latent = h_vals / 2.0  # scale for sigmoid
```

Remember: The key to beating the seed is STRUCTURED SPARSE FUNCTIONS, not smooth sigmoid curves from random normals.
