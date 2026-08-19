---
name: discovery-optimization
description: "Multi-variant search. Generate 5-10 diverse architectures per eval, implement all together with internal selection, evaluate once."
---

# Multi-Variant Search Protocol

## Per-Eval Strategy

Generate 5-10 CONCRETE variants:
1. Seed pattern variants: heights 1.4-1.8, widths at 20/30/40/60/80 percentiles
2. New architectures: narrow spike, wide plateau, bimodal, trimodal, smooth Gaussian, polynomial decay, asymmetric

Implementation: Define all variants, use internal argmax selection, evaluate best only.

Iteration: If architecture A wins, next eval: 60% from class A, 40% exploratory.

Key: BREADTH first, then DEPTH.
