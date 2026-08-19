---
name: new-family-exploration-protocol
description: Systematically explore entirely new function families after step functions fail.
---

# New Family Exploration Protocol for C2 Maximization

## Why Step Functions Are Stuck

The current best score of 1.03857 (vs seed 1.03841) shows that refining step functions yields diminishing returns. Step functions create "blocky" convolutions with sharp peaks that limit the ||f★f||₂²/||f★f||_∞ ratio.

## Phase 1: Diagnose with ANALYZE_CONVOLUTION

1. Call ANALYZE_CONVOLUTION on the current best function.
2. Study the smoothness_score (<0.3 = very blocky), l2_inf_ratio, and spectral_entropy.
3. IDENTIFY THE WEAKNESS: If smoothness is low, the problem is sharp transitions.

## Phase 2: Design Opposite Properties

Design a function class with DIFFERENT properties:

- **Gaussian Mixtures**: Smooth, multi-peaked, continuous derivatives
- **B-spline Basis**: Flexible smooth transitions with optimal control points
- **Oscillatory with Decay**: Structured convolutions from cosine modulations
- **Piecewise-Linear Smooth**: Linear segments instead of blocks

## Phase 3: Rapid Prototyping with Probe

1. Generate 3-5 variants from your new family.
2. Use PROBE_SOLUTION (30 budget!) to rank them quickly.
3. Select top 2-3 by probe score.
4. Evaluate only those that beat the current best probe score.

## Phase 4: Iterate Within Family, Then Switch

- If one family shows promise: refine it with small mutations (±5% parameters)
- After 3-4 iterations without beating the record: switch to a completely new family
- NEVER spend >5 iterations on a family that doesn't show promise

## Key Rule

OPPOSITE PROPERTIES WIN. If step functions are blocky, try smooth. If they're concentrated, try spread out. If they're monotonic, try oscillatory.
