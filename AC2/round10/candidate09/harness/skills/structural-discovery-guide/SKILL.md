---
name: structural-discovery-guide
description: Guide for discovering structurally novel C₂-improving functions. Prioritize complete functional form changes over parameter tuning.
---

# Structural Discovery for C₂ Maximization

## Why Structure, Not Parameters?
The current best step function (1.03431) is a LOCAL optimum. Small parameter tweaks keep you in this basin. You need GLOBAL escape via STRUCTURAL changes.

## Structural Change Categories

1. Multi-peak architectures: Instead of 1 central plateau, try 2-5 peaks with valleys
   - Example: Peak-Valley-Peak with heights 1.8, 0.3, 1.8
   - Breaks the "single mass" assumption of step functions

2. Asymmetric designs: Shift the center of mass
   - Left-heavy: mass concentrated in [0, 0.5]
   - Right-heavy: mass concentrated in [0.5, 1.0]
   - Skewed ramps (increasing then decreasing with bias)

3. Smooth transitions: Replace sharp steps with splines
   - B-splines with optimized knots
   - Cubic Hermite interpolations
   - Reduces numerical artifacts from discontinuities

4. Mixtures: Combine shapes
   - 0.7*step + 0.3*exponential_decay
   - 0.5*spline + 0.5*Fourier_mode
   - Create hybrid advantages

5. Variable complexity: Change discretization
   - 200-800 intervals (not just 450)
   - Non-uniform spacing (denser in important regions)

## Search Protocol

Phase 1 (Diversify): Generate 5-10 completely different FUNCTION FAMILIES. Probe each. Pick top 3.

Phase 2 (Confirm): Full evaluate the top probe candidates.

Phase 3 (Refine): Only now do small refinements within the winning family.

Phase 4 (Hop): After each eval, MAKE A MAJOR structural change (new family, asymmetry, multi-peak).

## Red Flags of Stagnation
- Same family for >10 iterations: CHANGE FAMILY
- Probe scores flat for 3 iterations: TRY DIFFERENT FUNCTION FORM
- Eval scores dropping: RESET to random diverse seed

## Target Outcome
Break through 1.035 by finding a function with fundamentally different structure than the seed.
