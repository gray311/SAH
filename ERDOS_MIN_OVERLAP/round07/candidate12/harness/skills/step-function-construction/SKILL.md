---
name: step-function-construction
description: Direct piecewise-constant step function construction for C₅ bound optimization. Avoids gradient descent traps by specifying h values explicitly.
---

# Direct Step Function Construction for C₅ Bounds

## Core Principle
Instead of optimizing latent → sigmoid, construct h directly as piecewise-constant with controlled support.

## Pattern Library

### Pattern 1: Single Support Interval
h = 1.0 on [0, 1.0], h = 0 elsewhere
- Integral = 1.0 ✓
- Simplest case, good baseline

### Pattern 2: Two Symmetric Supports
h = c on [0, 0.5] ∪ [1.5, 2.0], h = 0 elsewhere
- Set c = 1.0 to get integral = 1.0
- Spreads mass, potentially reduces max overlap

### Pattern 3: Three-Interval Alternating
h = c1 on [0, 2/3], h = c2 on [2/3, 4/3], h = c1 on [4/3, 2]
- Solve for c1, c2 to satisfy constraints
- Creates structure that may reduce correlation peaks

### Pattern 4: Tapered Decay
h = 2.0 - x on [0, 1.0], h = 0 on (1.0, 2.0]
- Linear decay from 2 to 1
- Smooth-ish but still piecewise

### Pattern 5: Concentrated Centers
h = 4.0 on [0.5, 0.75] ∪ [1.25, 1.5], h = 0 elsewhere
- Very narrow supports
- May create high peak overlaps

### Pattern 6: Sinusoidal Bins
Divide [0, 2] into n bins, set h[i] = a + b*sin(2*pi*i/n)
- Normalized so mean = 1/n
- Smooth variations over discrete supports

## Implementation Steps

1. **Choose pattern** from above or design new one
2. **Define breakpoints**: 0 = t₀ < t₁ < ... < tₙ = 2
3. **Set heights**: h[i] for each interval
4. **Verify constraints**: 
   - All h[i] ∈ [0, 1]
   - sum(h) * (2/n) = 1.0
5. **Compute C₅**: Use FFT correlation method
6. **Iterate**: Adjust breakpoints/heights based on score

## Common Pitfalls

- Forgetting to normalize for integral constraint
- Heights outside [0, 1] causing NaN in sigmoid
- Too many intervals causing numerical instability
- Not checking correlation at all lags (k=0 to N-1)

## Proven High-Quality Patterns

Start with these, then mutate:

1. **Single block**: [0,1]→1, [1,2]→0
2. **Dual blocks**: [0,0.5]→0.5, [0.5,1]→0, [1,1.5]→0, [1.5,2]→0.5
3. **Truncated uniform**: [0, 0.8]→1.25, [0.8, 2]→0 (then clamp to [0,1])
4. **Bimodal**: Two narrow peaks of height 2.0, width 0.5 each

## Optimization Within Pattern

Once pattern chosen:
- Optimize breakpoint positions
- Optimize relative heights (if multi-level)
- Try different discretizations (100, 200, 500 intervals)
