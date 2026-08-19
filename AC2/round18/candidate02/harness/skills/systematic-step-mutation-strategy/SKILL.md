---
name: systematic-step-mutation-strategy
description: Systematically explore step function parameter space (positions, heights, levels) before trying unrelated families. Use probes to filter.
---

# Systematic Step Mutation Strategy for C2 Maximization

## Why Steps First?
The seed's 12 step patterns are COMBINATORIAL solutions in a promising region. The local optimum is a valley in parameter space - we need to explore it systematically.

## Parameter Space Dimensions
- Positions: Each step boundary (±5%)
- Heights: Each level's value (±0.1 to ±0.2)
- Levels: Number of pieces (±1)
- Asymmetry: Mirror/reverse patterns

## Phase 1: Exhaustive Step Exploration

Iteration 1-5: Position-only mutations
- Generate 3 variants with position shifts
- Probe all, evaluate best 1

Iteration 6-10: Height-only mutations
- Generate 3 variants with height changes
- Probe all, evaluate best 1

Iteration 11-15: Level count mutations
- Generate 2 variants: +1 and -1 level
- Probe both, evaluate best

Iteration 16-20: Combined mutations
- Generate 2 variants with position + height
- Probe both, evaluate best

## Phase 2: Architecture Jump
If no improvement after 20+ step mutations:
1. Gaussian mixtures (2-3 Gaussians)
2. B-spline (50 control points)
3. Oscillatory decay

## Key Rule
NEVER abandon step functions until you've exhausted 15+ mutated variants. They're mathematically sound!
