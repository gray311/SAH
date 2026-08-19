---
name: constructive-patterns
description: Use direct construction over gradient descent. Enumerate combinatorial patterns. Test 5-20 candidates per eval.
---

# Constructive C5 Optimization

## Core Principle
Optimal step functions are LOW-DIMENSIONAL STRUCTURAL PATTERNS, not random functions.

## Pattern Library

Pattern A: Single Pulse
h(x)=1 on [0,1], h=0 elsewhere. Integral=1. ✓

Pattern B: Two Pulses
h(x)=a on [0,w], h=0. Choose a,w so a*w=1.
Try: a=0.5,w=2 or a=1,w=1.

Pattern C: Three-Level
Divide [0,2] into [0,2/3), [2/3,4/3), [4/3,2].
Heights from {0,0.5,1}. 27 combinations. Scale.

Pattern D: Symmetric Bimodal
h=1 on [a,1-a] ∪ [1+a,2-(1-a)].
Measure=2*(1-2a)=1 ⇒ a=0.25.
So: h=1 on [0.25,0.75] ∪ [1.25,1.75].

Pattern E: Center Concentrated
h=1 on [0.5,1.5], h=0. Integral=1. ✓

## Execution
1) Choose n=50 (coarse) or n=800 (refine)
2) For each pattern A-E:
   a) Construct h
   b) Verify ∫h=1 (scale)
   c) Clip to [0,1]
   d) Compute c5
3) Try random high-contrast patterns
4) Pick best candidate
5) If c5>0.380923, try finer n

## Key Insights
- Seed's 12 patterns are RANDOM; miss STRUCTURED solutions
- Optimal has SIMPLE SUPPORT (few non-zero intervals)
- SYMMETRY important
- Start COARSE (n=50), refine to n=800
- Enumerate DISCRETE HEIGHTS ({0,0.5,1}) first
- Best solution may be simple: h=1 on [0,1]
