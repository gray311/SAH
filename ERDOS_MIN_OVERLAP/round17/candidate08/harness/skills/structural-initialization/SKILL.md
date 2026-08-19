---
name: structural-initialization
description: Add wavelet bands, Fourier modes, piecewise linear, and multi-scale bump patterns to seed optimizer. Train each for 59000 steps.
---

# Structural Initialization - Erdos Problem

## Core Idea

The seed has 15 patterns but clusters. ADD new structural families:

### Wavelet-like (dyadic bands)
Alternating high-low bands at scales 4, 3, 5, etc.
- Creates orthogonal-like support regions

### Fourier modes
h(x) = sigmoid(sum freq*cos(2pi*k*x) * amplitude)
- Captures oscillatory patterns

### Piecewise linear
Linear ramps between breakpoints
- Simple, interpretable structures

### Multi-scale bumps
Nested Gaussians at different centers/scales
- Overlapping peaks create complex patterns

## Workflow

1. EDIT _get_best_initialization() in EVOLVE-BLOCK
2. ADD 1-2 new patterns from above families
3. Normalize: h = sigmoid(latent), then h /= (sum(h)*dx)
4. Ensure h in [0,1] (use clip if needed)
5. CALL evaluate_solution (59000 steps)
6. If no improvement, ADD MORE patterns

## Why This Works

- Diverse structures = better exploration of search space
- Each pattern is fresh, orthogonal starting point
- Seed training (59000 steps) is robust - trust it
- Focus on INITIALIZATION diversity, not training tweaks
