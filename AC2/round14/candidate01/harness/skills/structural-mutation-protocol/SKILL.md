---
name: structural-mutation-protocol
description: Systematic step-function mutation based on convolution structure.
---

# Structural Mutation Protocol

## Why Step Functions Work

Step functions achieve C₂ ≈ 0.896 because their convolutions have:
- Dominant central peak maximizing ||f★f||₂²
- Controlled tail decay keeping ||f★f||_∞ low
- Balanced L2/L∞ ratio

## Mutation Hierarchy (apply one at a time)

1. **Height Concentration** (first choice):
   - Increase highest step by 0.08-0.12
   - Decrease other steps proportionally
   - Example: [1.40, 1.40, 1.40] → [1.32, 1.56, 1.28]
   - Rationale: concentrates mass at convolution peaks

2. **Core Width Expansion**:
   - Expand main step by 5-8%
   - Contract wings by similar amount
   - Rationale: increases ||f★f||₂² more than ||f★f||_∞

3. **Symmetry Breaking**:
   - Make heights asymmetric: e.g., 1.40, 1.48, 1.32
   - Shift left/right portions by 2-3%
   - Rationale: breaks destructive interference patterns

4. **Localized Enhancement**:
   - Add bump at 35-40% position
   - Height: 0.3-0.5 relative to base
   - Width: 8-15 intervals
   - Rationale: exploits natural secondary convolution peaks

5. **Multi-Level Refinement**:
   - Add intermediate level between core and wings
   - Example: [0.55, 1.40, 2.15, 1.40, 0.55]
   - Fine-tunes convolution shape

## Execution Protocol

1. Call analyze_convolution_structure after combined_score > 1.02
2. Pick ONE mutation type, generate 3-5 variants
3. Probe ALL variants (use 30 probes total)
4. Full-eval only if probe > current best
5. If improvement: continue with same mutation type
6. If 3+ types fail: try different type or switch architectures
7. After 10 iterations with no gain: try new architecture (Gaussian, spline, etc.)

Key: ONE MUTATION TYPE AT A TIME + PROBE FILTERING = EFFICIENT SEARCH.
