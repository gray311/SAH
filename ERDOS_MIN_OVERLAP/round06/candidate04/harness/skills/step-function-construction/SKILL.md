---
name: step-function-construction
description: Use this when the seed's gradient descent fails. Direct construction of piecewise constant step functions often finds better solutions for the Erdős problem than gradient-based optimization.
---

# Direct Construction for C₅ Problem

## Core Principle

Instead of gradient descent, manually construct candidate step functions
with known good properties for minimizing max overlap.

## Construction Patterns

### Step Functions
- h=1 on [0,1], h=0 elsewhere: simple, satisfies ∫h=1
- h=2 on [0,0.5]: concentrated mass at start

### Symmetric Patterns
- Plateau: constant value on central interval
- Two spikes: mass concentrated in two regions

### Piecewise Linear
- Triangle: ramps up then down
- Ramp: linear increase or decrease

## Integration Constraint

Always verify ∫h=1: adjust heights or widths accordingly.
For N intervals over [0,2]: sum(h) * (2/N) = 1
