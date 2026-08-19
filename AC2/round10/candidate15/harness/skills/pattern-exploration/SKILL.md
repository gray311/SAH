---
name: pattern-exploration
description: Systematic exploration of novel step function architectures for C₂ maximization. Focus on structural innovation - different level counts, asymmetric distributions, bimodal shapes, extreme height contrasts.
---

# Pattern Exploration for C₂ Optimization

## Why Novel Patterns?
The seed's 13 patterns are local optima. To beat 1.03492, you need NEW architectures.

## Exploration Strategy

1. **Multi-Level Architecture** (5-7 levels)
   - More flexibility than seed's 3-5 levels
   - Example: 0.6 → 1.3 → 1.9 → 1.4 → 2.3 → 0.9
   - Allows fine-grained shape control

2. **Asymmetric Distributions**
   - Left-heavy: tall narrow left, short wide right
   - Right-heavy: opposite
   - Test split points: 0.3, 0.4, 0.6, 0.7

3. **Bimodal/Brittle Shapes**
   - Two peaks with valley: captures multi-modal optimization
   - Heights: 2.3 (peak1), 0.7 (valley), 2.3 (peak2)

4. **Extreme Contrast**
   - Very high narrow peak (2.5-2.8) with low wings (0.6-0.9)
   - Tests if sharp concentration helps C₂

5. **Plateau Shapes**
   - Flat top (1.6-2.0) with gradual ramps
   - Tests if smooth transitions help

## Process
1. Design 3-5 patterns using different strategies above
2. Probe all to rank
3. Evaluate top 1-2
4. If promising, do targeted refinement

## Key Insight
Don't tune old patterns. Generate new ones with fundamentally different structures.
