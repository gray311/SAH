---
name: family-switching-protocol
description: Escape local optima by switching function families. Try Gaussian, B-splines, or hybrids.
---

# Multi-Family Optimization Protocol

## Core Principle
The seed's step patterns are a LOCAL optimum. Explore new architectures.

## Phase 1: Family Exploration (iterations 1-10)
1. Call generate_function_family for a new family type
2. Generate 3 variants with structural differences
3. Probe all 3, evaluate best if probe >= 1.0

## Phase 2: Family-Specific Optimization (iterations 11-20)
- Optimize within family using JAX gradients
- For smooth families: optimize mu, sigma, weights, knots
- If no improvement in 3 iterations: switch families

## Phase 3: Final Refinement (iterations 21-30)
- Blend two good candidates or reinitialize 50% of parameters
- Probe 2-3 final variants, evaluate best

## Key Rules
- ALWAYS call generate_function_family - never stay in same family twice
- Use probes: 5-6 per iteration
- Structural changes beat parameter tweaks
