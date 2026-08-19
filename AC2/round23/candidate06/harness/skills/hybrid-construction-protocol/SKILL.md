---
name: hybrid-construction-protocol
description: Protocol for constructing hybrid functions - smooth edges, multi-scale superposition, polynomial modulation. Escape step-function local optimum.
---

# Hybrid Construction Protocol for C2 Maximization

## Core Idea
Step functions saturate. Escape by blending smooth transitions with step-like structure.

## Construction Templates

Template A: Smooth-Edge Steps
- Replace sharp jumps with sigmoid: f(x) = sigmoid(-2.0*(x - edge) / width)
- Width = 5-10% of peak region
- Preserves step-like concentration while adding smoothness

Template B: Multi-Scale Superposition
- f_total = base_pattern + alpha * scaled(base, scale=2.0) + beta * scaled(base, scale=0.5)
- alpha, beta ∈ [0.1, 0.4]
- Combines coarse and fine structure

Template C: Polynomial-Modulated Steps
- f(x) = step(x) * (1 - |x - center|/L)^p
- p ∈ [1.0, 2.5] controls decay smoothness
- Creates natural envelope around step region

## Execution Flow
1. Call analyze_structure to get current peak width, edges
2. Choose template based on structure: smooth if edges sharp, superposition if single peak
3. Generate 3 variants using different parameter settings
4. Probe all 3, evaluate best

## Key Rules
- Always smooth, never sharper (sharper = worse than step already)
- Multi-scale beats single-scale
- Probe before evaluating (30 probe budget total)
