---
name: discovery-optimization
description: "Precision tuning for FFT-based C2 optimization. Start with discretization and integration method changes,\nthen refine shapes, then expand architectures only if needed."
---

# Precision-Tuned C2 Maximizer

## Why Precision Matters
The seed achieves 1.042 combined_score, meaning it's already near-optimal. Small improvements
come from better convolution resolution and numerical integration, not radical architecture changes.

## Phase 1: Precision Tuning (iterations 1-2)

Step 1: Analyze Current Best
- Call analyze_convolution_profile
- Note: Where is ||f*f||_2 concentrated? What's the resolution?

Step 2: Try Discretization Changes
- INCREASE num_intervals: 800, 1000, or 1200 (better FFT resolution)
- Check integration: Simpson's rule h/3 * (y1^2 + y1*y2 + y2^2)
- These are SAFE mutations that often yield 0.1-0.3% improvements

Step 3: Probe and Evaluate
- Call probe_solution on all variants
- Evaluate only those with probe combined_score > 1.0

## Phase 2: Shape Refinement (iteration 3)

Only if Phase 1 didn't beat record:
- Mutate step boundaries: shift by ±2% of total range
- Adjust heights by ±0.05 (keep f ≥ 0)
- Probe all, evaluate best

## Phase 3: Architecture Expansion (only if stuck)

If still no improvement after 2 full evals:
- Add one asymmetric level to step function
- OR switch to simple Gaussian mixture (2-3 peaks)
- Evaluate top 1

## Key Rules
- PROBE ALL before any full eval (30 probe budget)
- Evaluate max 3 variants total
- NEVER try radical architecture changes first
- Always analyze convolution profile to guide mutations
