---
name: discovery-optimization
description: "Optimize C\u2082 via structural architectural search. Analyze current patterns, test diverse function classes (asymmetric, multi-peak, varying resolutions), and only evaluate best variants."
---

# C₂ Architectural Search

## Phase 1: Analysis
Call analyze_step_params once to extract current heights, widths, and positions.
Note which parameters are most constrained.

## Phase 2: Broad Exploration
Test ARCHITECTURAL variants, not parameter tweaks:
- **Resolution changes**: 300, 450, 600, 900 intervals
- **Asymmetric patterns**: Split at 0.2/0.6 instead of 0.25/0.75
- **Multi-peak designs**: 2-peak, 3-peak, 4-peak functions
- **Plateau variants**: Flat-topped instead of peaked
- **Logarithmic spacing**: Steps at positions derived from log scale

For each variant:
1. Edit solution with new architecture
2. Probe all variants (3-5 probes per variant)
3. Keep best probe score
4. Evaluate once

## Phase 3: Stagnation Recovery
If no improvement after 8 iterations:
1. Call try_new_architecture with a completely new function class
2. Examples: Gaussian mixture, spline-based, Fourier-based

## Phase 4: Refinement
Only after finding a new architecture, do small parameter tuning.

## Critical Rules
- Always analyze BEFORE editing
- Always probe BEFORE evaluating
- Test 5-10 diverse architectures per run
- Evaluate only the single best probe result
- If score drops, the architecture failed - try a different class
