---
name: discovery-optimization
description: "Optimize C2 by enhancing the seed's JAX optimizer with diverse initialization families.\nUse step_config_generator to create hybrid functions. Probe early, eval late. Max 4 evals."
---

# C2 Optimization: Enhanced Seed Strategy

## Core Principle

The seed uses gradient descent with 9 initializations. DO NOT replace this with manual step functions.
Instead, augment it with better initialization strategies.

## Phase 1: Generate New Initializations

Use step_config_generator to create hybrid functions:

1. Bimodal bumps: two Gaussian-like peaks

2. Asymmetric triangles: rising/falling slopes of different steepness

3. Plateau functions: flat top with sloped sides

4. Multi-hump: 3-4 peaks of varying widths

## Phase 2: Probe-Based Selection

1. For each new initialization, run optimizer for 1000 steps (partial run)
2. Call probe_solution to check C2
3. If probe C2 > 1.026: proceed to full optimization
4. If probe C2 <= 1.026: discard and try next

## Phase 3: Full Optimization

1. Take top 2 candidates from Phase 2
2. Run seed's optimizer for full 40000 steps
3. Evaluate with evaluate_solution
4. If no improvement after 2 evals: try polynomial tails

## Phase 4: Hybrid Functions

If pure steps fail, try:
- Step function with smooth edges
- Step + exponential tail

## Critical Rules

- MAX 4 full evaluations
- Always run seed's optimizer (don't manually construct final f)
- Probe after partial optimization, not on raw constructions
- Use step_config_generator for structured exploration
