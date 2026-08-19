---
name: step-tail-exploration
description: Explore tail behaviors for step functions - extended support, asymmetric decay, double-tailed structures. Use all 30 probes before full evaluation.
---

# Step-Tail Exploration Protocol for C2 Maximizer

## Core Principle
The seed's step functions work (1.042 score). Explore TAIL BEHAVIORS to find better patterns:
- Extended support: [-4, 4] instead of [-3, 3]
- Asymmetric decay: different left/right tail behaviors
- Double-tailed: small tails at both ends

## Tail Modes to Explore
1. **Extended Support**: num_intervals=800, support [-4, 4]
   - Rationale: More room for convolution structure
   - Try heights: 1.0-2.0 in center, 0.3-0.5 in tails
2. **Asymmetric Left**: start at 0.15*n, peak at 0.5*n, end at 0.85*n
   - Rationale: Test if asymmetry helps
   - Heights: [0.5, 1.5, 2.2, 1.5, 0.5]
3. **Asymmetric Right**: start at 0.25*n, peak at 0.5*n, end at 0.80*n
   - Rationale: Opposite asymmetry test
4. **Double-Tailed**: small tails [0.3, 0.3] at both ends
   - Rationale: Test if edge contributions help

## Execution Flow
1. Call analyze_step_patterns to understand current structure
2. Call generate_candidates with DIFFERENT tail modes
3. Call probe_inverted_tail to test inverted tail hypothesis
4. Call probe_solution on ALL variants (use all 30 probes)
5. Evaluate only if probe >= 1.0
6. If no improvement after 10 iterations: try EXTENDED SUPPORT

## Key Rules
- STAY IN STEP-FUNCTION SPACE
- Use 30 probes to explore 15-20 variants
- NEVER generate Gaussian, B-spline, or oscillatory functions
- Focus on TAIL BEHAVIORS, not arbitrary mutations
