---
name: structural-pattern-search
description: Method for finding Erdős C5 minimizers via discrete structural search. Prioritize piecewise-constant patterns over gradient descent. Use probe-first screening.
---

# Structural Pattern Search for Erdős C5

## Overview
The optimal step function has piecewise-constant structure. This skill guides systematic exploration of such patterns.

## Phase 1: Structural Understanding
1. Call analyze_structure ONCE to get discretization geometry
2. Note: dx = 2.0 / num_intervals ≈ 0.0025 for 800 intervals
3. Thresholds are in [0, 2] space

## Phase 2: Pattern Generation
For each pattern family:
1. Define the structural formula explicitly
2. Parameterize with 1-3 key variables
3. Use probe to screen before full eval

## Phase 3: Systematic Search Order
Priority (based on theoretical likelihood):
1. Symmetric threshold (single pulse, centered)
2. Asymmetric thresholds (mass in left/right halves)
3. Double/three-pulse configurations
4. Sin/cos based smooth-to-step conversions
5. Gradient solution thresholding

## Phase 4: Probe-Gated Evaluation
- Probe every variant immediately after editing
- Only full eval if probe > 0.4 × base_score
- This saves ~20 evals for screening

## Phase 5: Parameter Perturbation
When a pattern shows promise:
1. Vary one parameter at a time
2. Use golden-section search over key parameter
3. Keep modifications structural (not tiny gradient steps)

## Key Constraints Checklist
[ ] Integral(h) × dx = 1.0 (critical!)
[ ] h values in [0, 1]
[ ] Program doesn't error on eval
[ ] Score improvement tracked vs seed

## Stop Conditions
- 25 iterations with no progress: abandon pattern class
- Best probe < 0.3 × base: switch strategy
- Clear improvement: fine-tune or finish
