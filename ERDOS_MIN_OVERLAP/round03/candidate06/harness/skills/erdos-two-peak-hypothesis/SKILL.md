---
name: erdos-two-peak-hypothesis
description: Hypothesis - Best C5 solutions have two asymmetric peaks at x≈0.25 and x≈1.75. LEFT peak should be NARROWER (width≈0.12) than RIGHT (width≈0.18) to reduce overlap. Start with this asymmetric construction, then refine peak widths in ±0.015 steps. Target c5_bound < 0.380923.
---

# Erdos C5: Two-Peak Asymmetric Hypothesis

## Key Insight
The minimum overlap occurs when peaks are ASYMMETRIC:
- Left peak at x=0.25 with width w_left ≈ 0.12
- Right peak at x=1.75 with width w_right ≈ 0.18
- This reduces h(x)(1-h(x+k)) overlap for small k

## Search Strategy
1. Start with w_left=0.12, w_right=0.18 (baseline asymmetric)
2. Refine: vary w_left in [0.10, 0.14] and w_right in [0.16, 0.20]
3. Use probe to quickly rank 9-16 combinations
4. Keep best 2-3 for full optimization

## Parameter Grid for Systematic Search
- w_left: 0.10, 0.12, 0.14 (3 values)
- w_right: 0.16, 0.18, 0.20 (3 values)
- Total: 9 combinations to probe, then optimize top 3

## Expected Improvement
Asymmetric peaks reduce correlation at small shifts, lowering C5 bound.
Symmetric peaks (w_left=w_right) are suboptimal for this domain.

## Implementation Notes
- Use gaussian peaks for smooth transitions
- Normalize so ∫h = 1 (sum(h) * dx = 1)
- Apply sigmoid in seed program's _objective_fn
- Monitor integral constraint: if |∫h - 1| > 0.01, increase penalty
