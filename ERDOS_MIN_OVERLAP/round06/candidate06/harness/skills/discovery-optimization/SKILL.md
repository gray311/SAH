---
name: discovery-optimization
description: "Erd\u0151s C\u2085 bound optimization. Find step functions minimizing max overlap. Use explicit construction + probe ranking to beat 0.3809."
---

# Erdős C₅ Problem: Explicit Step Function Construction

## Problem
Minimize: max_k ∫₀² h(x)(1-h(x+k))dx
Subject to: h:[0,2]→[0,1], ∫h=1

## Why Gradient Methods Fail
The seed's Adam optimizer gets trapped because the optimal h has a specific discrete structure. You need to CONSTRUCT candidate solutions explicitly.

## Strategy: Concrete Step Function Designs

### Design 1: Single Block
h(x) = 1 for x∈[0,1], h(x) = 0 otherwise. But we need ∫h=1, so this works!
c5_bound for this: max_k ∫₀² h(x)(1-h(x+k))dx

### Design 2: Double Block
Split the unit mass into two intervals. Try:
- h = 0.5 on [0,1], h = 0.5 on [1,2] (uniform)
- h = 1 on [0,0.5], h = 0 on [0.5,1.5], h = 1 on [1.5,2] (two blocks)

### Design 3: Symmetric Triple Block
- h = 1 on [0,a], h = 0 on [a,2-a], h = 1 on [2-a,2] where a = 0.25
- Adjust a so ∫h = 1: 2a = 1 ⇒ a = 0.5

### Design 4: Asymmetric Patterns
- Mass concentrated near x=0 and x=2
- Three blocks with different widths

## Execution Plan

1. **Probe Phase**: Construct 5-10 explicit step functions, use probe_solution to rank them
2. **Refine**: Take top 2, adjust breakpoint positions, probe again
3. **Eval**: Once you find c5_bound < 0.3809, do full eval
4. **Iterate**: Try variations: different numbers of blocks, asymmetric splits

## Implementation Template

In EVOLVE-BLOCK, replace the multi-restart optimizer with:
- A function that explicitly constructs step functions given breakpoint locations
- A search loop that tries different breakpoint configurations
- Use jnp.searchsorted or manual breakpoints for piecewise constant functions

## Important
- Use probe_solution for cheap ranking (30 free probes!)
- Focus on SIMPLE structures (2-5 intervals), not complex smooth functions
- Always ensure ∫h=1 by choosing breakpoints appropriately
- If you get stuck, try: single block, double block, symmetric triple block
