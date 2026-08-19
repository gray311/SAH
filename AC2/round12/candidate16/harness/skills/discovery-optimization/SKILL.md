---
name: discovery-optimization
description: "Bold combination mutations for C\u2082 maximization. Instead of gradual single-parameter tweaks, apply coordinated changes (height+width+position together) that break out of local optima. Target high-peak regimes and asymmetric architectures."
---

# Bold Combination Mutation Protocol

## Why This Works

The seed's 13 step patterns are near a local optimum. The C₂ landscape is extremely flat at this precision (differences of 0.0001 matter). Single-parameter tweaks can't escape. You need coordinated changes that break the optimization basin entirely.

## Mutation Strategy: Combinations, Not Singles

Don't try one change at a time. Apply 3-4 coordinated mutations in a single edit:

### Combination Type 1: High-Peak + Width + Shift
- Increase central peak by 0.15-0.20 (from 1.6 to 1.75-1.80)
- Expand central interval by 10-12%
- Shift entire pattern right by 0.02-0.03
- Rationale: Higher peak boosts L2 norm; wider support increases overlap; asymmetry breaks perfect interference

### Combination Type 2: Extreme Asymmetry
- Central peak: 2.0-2.2
- Left wings (2 levels): 0.7, 0.9
- Right wings (2 levels): 0.9, 1.0
- Rationale: Breaking symmetry reduces infinity norm at expensive points while maintaining L2

### Combination Type 3: Double-High-Peak Architecture
- Two prominent peaks at 25% and 75%: both 1.8-1.9
- Four small wings: 8%, 12%, 18%, 24% at 0.7, and 85%, 92%, 94%, 96% at 0.6-0.7
- Rationale: Multiple high peaks can beat single-peak architectures through constructive interference patterns

### Combination Type 4: Smooth Transition Multi-Level
- Keep 13-level structure but with gradual height changes (not flat steps)
- Heights: 0.65 to 0.75 to 0.85 to 0.95 to 1.1 to 1.3 to 1.5 to 1.65 to 1.8 to 1.65 to 1.5 to 1.3 to 1.1 to 0.95 to 0.85 to 0.75 to 0.65
- Rationale: Smooth transitions might reduce high-frequency artifacts in convolution

## Execution Plan

1. Attempt 1-2: Pick Combination Type 1, implement with edit_solution, evaluate once
2. Attempt 3-4: Pick Combination Type 2, implement, evaluate once
3. Attempt 5-6: Pick Combination Type 3 or 4, implement, evaluate once
4. Decision: If best improvement < 0.0005, discard the entire multi-level paradigm and explore smooth functions or Fourier-space approaches
5. Never spend 5+ evals on variants of the same combination

## Key Differences from Seed

- Seed: 13 flat steps with tiny perturbations
- You: 3-5 coordinated changes per edit, larger changes (0.15+ on heights), focus on HIGH-PEAK regime
- Seed: 13 patterns tried sequentially
- You: 4-6 bold combinations tried in parallel, then abandon and explore new paradigm

## When to Abandon Current Approach

After 6 evals with no improvement > 0.0005 over seed, try:
- Smooth Bell curves (Gaussian-like) with optimized sigma and amplitude
- Piecewise-linear triangles instead of rectangles
- Fourier-synthesis functions with 3-5 harmonics
