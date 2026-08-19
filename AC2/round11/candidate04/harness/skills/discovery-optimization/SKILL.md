---
name: discovery-optimization
description: "Mathematically-grounded pattern synthesis for C\u2082 maximization. Use pattern_analysis to understand current patterns, then pattern_synth to generate executable code for new architectures (asymmetric multi-peaks, spline transitions, irregular configurations). Focus on discovering entirely new patterns."
---

# C₂ Maximizer: Pattern Synthesis Protocol

## Phase 1: Structural Analysis (first iteration only)

1. Call pattern_analysis to extract current pattern characteristics:
   - Height range and average
   - Number of levels
   - Symmetry properties
   - Peak positions

2. Identify weak points:
   - Where ||f★f||∞ might be inflated (too concentrated peaks)
   - Where ||f★f||₂² could be increased (smoothness, spread)

## Phase 2: Pattern Synthesis

Use pattern_synth to generate CONCRETE CODE for new patterns. Don't just tweak parameters.

**NEW ARCHITECTURES TO SYNTHESIZE**:

1. **Asymmetric Multi-Peak**: 3-5 peaks with unequal heights breaking symmetry
   Example heights: [0.5h, 1.5h, 0.3h, 1.2h, 0.4h]

2. **Smooth Transition**: Replace hard steps with exponential-like decay segments
   Example: use softplus or sigmoid transitions between levels

3. **Centered Dominant Peak**: Tall central peak with smaller asymmetric wings
   Example: [0.3h, 1.7h, 0.25h, 1.3h, 0.25h]

4. **Irregular Spacing**: Non-uniform interval widths (15-30% variation)
   Example: vary interval boundaries at 0.08n, 0.22n, 0.38n, etc.

5. **Bi-modal Distribution**: Two distinct peaks with valley in between
   Example: [1.0h, 0.1h, 1.8h, 0.1h, 1.0h]

## Phase 3: Evaluation Strategy

1. Generate ONE concrete pattern via pattern_synth
2. Evaluate it with evaluate_solution (probe is unreliable)
3. If successful: synthesize more variants in that architecture
4. If failed: analyze why and synthesize a different architecture

## Key Principles

- DIVERSITY over refinement: New architectures beat better parameters
- ONE eval at a time: Test one pattern, learn, then try another
- CODE is king: pattern_synth returns executable code, not descriptions
- Math matters: Understand WHY a pattern should work before synthesizing it
