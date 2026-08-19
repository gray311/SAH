---
name: c5-explicit-constructions
description: Method playbook - construct explicit step functions with integral=1. Prioritize simple patterns. Validate before evaluation. Use probes.
---

# C5 Optimization: Explicit Construction

Problem: Find h:[0,2]->[0,1], integral(h)=1, minimize max overlap.

Patterns:
1. Single interval: h=1 on [0,1], 0 elsewhere. Integral=1.0
2. Uniform: h=0.5 everywhere. Integral=1.0
3. Two bumps: h=1 on [0,0.5] U [1,1.5]. Integral=1.0
4. Centered: h=2/3 on [0.25,1.75]. Integral=1.0
5. Four sections: h=0.5 on each quarter. Integral=1.0

Steps:
1. Implement ONE pattern
2. Verify: h in [0,1], sum(h)*dx=1.0
3. If invalid, fix before evaluating
4. Evaluate and record combined_score
5. Use probe_solution for variants

Key: Explicit > gradient descent. Simpler beats complex.
