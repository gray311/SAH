---
name: discovery-optimization
description: "Edit seed initialization patterns to explore structural diversity: wavelet bands, Fourier modes, piecewise linear, multi-scale bumps. Train each candidate for 59000 steps."
---

# Structural Initialization for Erdos Problem

## Problem
Seed has 15 patterns but they cluster around similar structures. Need MORE structural diversity.

## Solution: ADD New Initialization Families

### Pattern 1: Wavelet-like (dyadic bands)
for scale in [4, 3, 5]:
    h = np.zeros(N)
    step = 2.0 / scale
    for i in range(int(N // (2*scale))):
        band_start = int(i * 2 * step * N)
        band_end = band_start + int(step * N)
        h[band_start:band_end] = 4.0

### Pattern 2: Fourier modes
total = np.zeros(N)
for freq, amp in [(1, 0.8), (3, 0.5), (5, 0.3)]:
    total += amp * np.cos(2 * np.pi * freq * np.arange(N) / 2.0)
h = jax.nn.sigmoid(total)
h = h / (np.sum(h) * dx)

### Pattern 3: Piecewise linear
h = np.zeros(N)
h[:int(0.3*N)] = 3.0
h[int(0.3*N):int(0.6*N)] = np.linspace(3.0, 0.5, int(0.3*N))
h[int(0.6*N):] = 0.5
h = h / (np.sum(h) * dx)
h = np.clip(h, 0.01, 1.0)

### Pattern 4: Multi-scale bumps
h = np.zeros(N)
for center, width in [(0.4, 0.05), (1.0, 0.15), (1.6, 0.03)]:
    pos = int(center * N)
    for k in range(-int(N*width), int(N*width)+1):
        h[pos+k] += 6.0 * np.exp(-((k) / (N*width))**2)
h = h / (np.sum(h) * dx)

## Workflow

1. ADD 1-2 new patterns to seed's _get_best_initialization method
2. Each pattern: ensure h in [0,1] and integral=1
3. CALL evaluate_solution (59000 steps each)
4. If no improvement, ADD MORE patterns or MODIFY structure

## Key Points

- Seed training is robust (59000 steps) - focus on INITIALIZATION diversity
- Each new pattern is a fresh starting point
- Use create_structural_init to generate diverse screened candidates
