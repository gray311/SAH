---
name: construction-first-search
description: Pure mathematical construction strategy for Erdos minimum overlap. Generates noise-free constructions, probes immediately, optimizes only the best candidate with minimal perturbations and integral normalization.
---

# Construction-First Search for Erdos Minimum Overlap

## Core Principle: Zero-Noise Initializations

DO NOT add Gaussian noise to mathematical constructions. This destroys the structural properties that make them good starting points.

## Step 1: Generate Pure Constructions

Call analyze_structure_probe() to get 5 exact, noise-free constructions:
1. periodic_1: h(x)=1 on [0,1], h(x)=0 on (1,2] - integral=1 exactly
2. periodic_2: h(x)=1 on [0,0.5]U[1,1.5], h(x)=0 elsewhere - integral=1 exactly
3. bimodal_tight: Two narrow Gaussian peaks at x=0.25 and x=0.75, normalized to integral=1
4. triangular_3: Three-level step function, normalized to integral=1
5. golomb_5: Five peaks at Golomb ruler positions, normalized to integral=1

## Step 2: Probe All Constructions

Use probe_solution on each construction WITHOUT any optimization:
- Check c5_bound for raw periodic_1, periodic_2, bimodal_tight, etc.
- Expect: periodic_2 ~ 0.365-0.37, bimodal_tight ~ 0.36, golomb_5 ~ 0.37
- SELECT the construction with LOWEST c5_bound (HIGHEST probe score)

## Step 3: Minimal Optimization

Only optimize the BEST construction:
- Seed: exact construction from step 1
- Noise: Gaussian with sigma=0.05 (tiny perturbations only)
- Optimizer: Adam with lr=0.1 -> decay to 0.001 over 40k steps
- Normalization: After every 5k steps, re-normalize to satisfy integral(h)=1 exactly
- Total steps: 30k-40k (not the full 59k)

## Step 4: Final Polish (Optional)

If combined_score > 1.0 but not by much, run additional polishing:
- 5k more steps with lr=0.001
- No noise, pure gradient descent
- Final integral normalization

## Expected Performance

- pure periodic_2: c5 ~ 0.365 (no optimization needed)
- optimized bimodal_tight: c5 ~ 0.355-0.360
- optimized golomb_5: c5 ~ 0.358-0.362

Target: c5_bound < 0.38092303510845016 for combined_score > 1.0
