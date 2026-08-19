---
name: discovery-optimization
description: "Generate structurally diverse, valid initializations for Erdos optimization. Use jump_to_pattern tool to create candidates with integral=1 and varied structures."
---

# Jump-to-Pattern Strategy

The seed optimizer trains for 59000 steps on a single latent vector.
To find improvements, we need to try MANY different structural patterns.

## Tool: jump_to_pattern

This tool creates valid step functions (integral=1) with specific structures:
- Two-level (bipartite): h takes two values, heights adjusted for integral=1
- Three-level: three regions, heights adjusted for integral=1  
- Golomb-like: peaks at specific marks, heights adjusted for integral=1
- Sinusoidal-modulated: sin/cos waves + noise, heights adjusted for integral=1

Each candidate returns c5_bound (analytical, no training needed).

## Workflow

1. CALL jump_to_pattern(structure="two-level", seed=0)
2. CALL jump_to_pattern(structure="three-level", seed=1)
3. CALL jump_to_pattern(structure="golomb", seed=2)
4. CALL jump_to_pattern(structure="sinusoidal", seed=3)

5. Analyze c5_bound from each candidate
6. CALL evaluate_solution on all candidates with c5 < 0.36

7. If no improvement, try different structures or higher temperature

## Why this works

- Guarantees integral=1 (validity constraint satisfied by construction)
- Structural diversity: different patterns may be optimal
- Precomputed c5: fast screening, no training needed
- Budget-efficient: 4 tool calls, 3-6 full evals
