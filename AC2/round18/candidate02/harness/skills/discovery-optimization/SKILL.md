---
name: discovery-optimization
description: "Step-parameter exploration with systematic mutation. Extract parameters from current best using step_pattern_analyzer, generate mutated variants with position/height/level variations, use probes to filter. Only try different families after exhausting step-parameter search space."
---

# Step-Parameter Exploration Protocol for C2 Maximization

## Core Principle
The seed's 12 step patterns are COMBINATORIAL solutions in a promising region. Systematic parameter exploration (positions, heights, number of levels) can escape the local optimum better than jumping to unrelated families.

## Phase 1: Systematic Step Mutation (iterations 1-20)

Step 1: Analyze Current Best
- Call step_pattern_analyzer on your best function
- Extract: number of levels, heights, positions, widths

Step 2: Generate Mutated Variants
- Create 8-12 variants with systematic changes:
  * Position shifts: ±5% of interval width
  * Height variations: ±0.1 to ±0.2 from original
  * Level count: ±1 additional level (split or merge)
  * Asymmetry: mirror/reverse some patterns
- Keep all variants non-negative with jnp.maximum(f, 0) or jax.nn.softplus

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 8-12 variants
- Call evaluate_solution on TOP 2 by probe score
- If probe score < 1.0: skip full eval, try next

Step 4: Iterate
- Continue with different mutation types each iteration
- If 15+ variants exhausted without improvement: switch to Phase 2

## Phase 2: Architecture Exploration (iterations 21-30)

Only if Phase 1 yields no improvement:
1. Try Gaussian mixtures: 2-3 Gaussians with optimized means/stds
2. Try B-spline: 50 control points with softplus positivity
3. Try oscillatory decay: (1+alpha*cos(beta*x))*exp(-gamma*|x|)

For each family: generate 3 candidates, probe all, evaluate top 2

## Key Rules
- STEP MUTATION FIRST (proven region, combinatorial search)
- Use 30 probes to explore 15-20+ variants before full evaluations
- Only abandon steps after exhausting mutation space
- Always analyze current best before generating mutations
