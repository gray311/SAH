---
name: step-function-strategy
description: Use discrete step functions (rectangular pulses, Heaviside) instead of smooth Gaussians. Enforce integral=1 strictly with high penalties. Multi-phase optimization.
---

# Step Function Strategy for Erdos Minimum Overlap

## Why Step Functions?
The optimal h(x) is a DISCRETE STEP FUNCTION, not a smooth curve.
Use rectangular pulses and sharp transitions.

## Construction Templates

### Bimodal Rectangular
h(x) = 1 for x in [0, w1] ∪ [2-w2, 2], h=0 elsewhere
Choose w1=w2=0.22, with small overlap adjustment

### Trimmed Bimodal
h=1 on [0, 0.2], h=0.5 on [0.2, 0.6], h=0 on [0.6, 2]
Integral = 0.2 + 0.4 = 0.6 + 0.4 = 1.0

### Three Equal Pulses
Three pulses of width 1/3 each, h=1
Total width = 1, integral = 1

## Optimization Protocol

### Phase 1: 8000 steps
- lr = 0.01
- penalty = 200000
- Target: reduce integral error to < 0.001

### Phase 2: 20000 steps
- lr = 0.003
- penalty = 1000000
- Target: minimize c5_bound

### Phase 3: Optional fine-tune
- 5000 steps
- lr = 0.001
- penalty = 2000000

## Before Submitting
ALWAYS verify:
1. integral(h) is within 0.001 of 1.0
2. c5_bound < 0.380923
3. combined_score > 1.0
