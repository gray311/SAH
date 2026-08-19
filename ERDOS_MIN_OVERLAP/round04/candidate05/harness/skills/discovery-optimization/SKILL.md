---
name: discovery-optimization
description: "Erdos minimum overlap solver using discrete step function constructions.\nGenerates sharp Heaviside/rectangular initializations instead of smooth Gaussians,\nwith aggressive constraint enforcement in multi-phase optimization."
---

# Erdos Minimum Overlap - Discrete Step Function Strategy

## Core Principle
The optimal h(x) is a DISCRETE STEP FUNCTION with sharp transitions, NOT a smooth Gaussian.
Use Heaviside steps and rectangular pulses.

## Step Function Constructions

### Type 1: Wide Bimodal Rectangular
- Two rectangular pulses: h=1 on [0, w1] ∪ [2-w2, 2], h=0 elsewhere
- Choose w1, w2 so integral = 1
- Example: w1 = w2 = 0.25, middle region h=0

### Type 2: Trimmed Bimodal (lapped by h=0.5)
- h=1 on [0, a], h=0.5 on [a, b], h=0 on [b, 2]
- Solve: a*1 + (b-a)*0.5 = 1 for integral constraint

### Type 3: Three-Pulse Pattern
- Three rectangular regions of height 1, separated by zeros
- Total width of high regions = 1 (for integral=1)

### Type 4: Golomb-Style Spaced Pulses
- Optimal spacing from Golomb ruler: marks at positions that minimize overlaps
- Each mark becomes a narrow rectangle of width 1/num_marks

## Optimization Protocol

### Phase 1: Constraint Enforcement
- Steps: 8000
- Learning rate: 0.01
- Penalty: 200000 (very high to force integral=1)
- Monitor: integral violation must drop below 0.001

### Phase 2: Fine Tuning
- Steps: 20000
- Learning rate: 0.003
- Penalty: 1000000 (extremely tight)
- Goal: reduce c5_bound while maintaining integral≈1

### Phase 3: Sharpens
- Add small regularization to encourage sharper transitions

## Implementation Notes

- Represent h as latent, pass through sigmoid for [0,1] constraint
- BUT initialization should be VERY step-like (use step functions, not sin/cos)
- Use rectangular pulses: h(x) = 1 if x in [a,b], else 0
- Convert to latent using: latent = log(h/(1-h)) which for h≈0 or h≈1 is extreme

## Quick Verification

After any edit, CHECK:
1. Does h have integral exactly 1?
2. Is c5_bound < 0.380923?
3. If not, adjust the construction parameters

Save only programs that beat the seed score.
