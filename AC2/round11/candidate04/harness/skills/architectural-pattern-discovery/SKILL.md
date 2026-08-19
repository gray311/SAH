---
name: architectural-pattern-discovery
description: Systematic approach to discovering new C₂-optimizing pattern architectures. Analyze current patterns, synthesize new architectures (asymmetric, bi-modal, smooth transitions), and iterate based on evaluation feedback.
---

# Architectural Pattern Discovery for C₂ Maximization

## Core Principle

The seed's 13 step patterns are locally optimized. You need NEW ARCHITECTURES, not parameter tweaks.

## Protocol

### Step 1: Analyze Current Architecture
Call pattern_analysis to understand:
- Height distribution (range, std, symmetry)
- Number of unique levels
- Current pattern count

### Step 2: Select New Architecture Class
Choose from these proven classes:

1. **Asymmetric Multi-Peak**: Break symmetry with 3-5 peaks of unequal heights
   - Reduces ||f★f||∞ by avoiding constructive interference
   - Example: [0.4h, 1.5h, 0.5h, 1.3h, 0.4h]

2. **Smooth Transition**: Replace hard steps with exponential-like ramps
   - Smoother functions may have better L2 norm properties
   - Use jnp.linspace for controlled transitions

3. **Bi-Modal Distribution**: Two distinct peaks with valley between
   - Exploits convolution's peak-avoidance behavior
   - Heights: [high, low, high] pattern

4. **Irregular Spacing**: Non-uniform interval widths (15-30% variation)
   - Avoids constructive interference at regular intervals
   - Vary interval boundaries: 0.08n, 0.22n, 0.38n, etc.

5. **Tri-Modal Symmetric**: Three peaks, outer peaks smaller
   - Balances concentration with spread
   - Pattern: [low, mid, high, mid, low]

### Step 3: Synthesize and Evaluate
1. Call pattern_synth to generate CONCRETE code for chosen architecture
2. Implement ONE pattern (not multiple at once)
3. Evaluate with evaluate_solution
4. If successful: synthesize more variants in that class
5. If failed: try different architecture

### Step 4: Iterate and Refine
- Track which architecture classes improve C₂
- For successful classes: generate 2-3 more variants
- For failed classes: analyze why and try different parameters
- Never settle on small tweaks - aim for architectural breakthroughs

## Key Success Factors

- DIVERSITY: Explore fundamentally different pattern classes
- CONCRETENESS: Use pattern_synth's executable code, not descriptions
- ONE-AT-A-TIME: Test one pattern, learn, then try another
- PERSISTENCE: Try at least 5-7 different architectures before concluding
