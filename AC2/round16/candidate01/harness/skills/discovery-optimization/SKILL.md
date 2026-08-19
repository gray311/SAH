---
name: discovery-optimization
description: "Systematic step-pattern mutation for C\u2082 maximization. Use analyze_step_pattern to understand structure, then step_mutator to generate mathematically-informed mutations. Focus on small height/width changes before exploring hybrids."
---

# C₂ Optimizer: Systematic Step-Pattern Refinement Protocol

## Core Principle

The step-function record is LOCAL but achievable. To beat 1.03896, systematically refine step patterns with SMALL, targeted mutations. Smooth functions (Gaussian, splines) are LIKELY to underperform step functions for this ratio.

## Phase 1: Structural Analysis (Iteration 1)

1. Call analyze_step_pattern ONCE to extract: number of levels, height values, interval positions, symmetry properties

2. Identify "weak links": which level pairs could benefit from height adjustment? which intervals are too narrow/wide?

## Phase 2: Guided Mutation (Iterations 2-15)

Generate mutations in order:

**Mutation A: Height Perturbation** (most promising)
- Increase core level height by 0.02-0.06
- Decrease wing levels by 0.02-0.04
- Create asymmetry: left side +0.03, right side -0.02

**Mutation B: Width Expansion**
- Expand the widest interval by 5-8%
- Contract narrow intervals by 3-5%
- Keep total length constant

**Mutation C: Spacing Adjustment**
- Shift interval boundaries by 2-4% of domain
- Focus on breaking exact symmetry

**Mutation D: Level Addition**
- Split the middle interval into two with intermediate height
- Add one extra level (total goes from 4→5 or 5→6)

## Phase 3: Hybrid Patterns (Iterations 16-25)

If single-pattern refinement stalls:
- Combine two seed patterns (e.g., pattern 0 + pattern 2)
- Take left 40% of pattern A, right 60% of pattern B
- Smooth the transition zone

## Phase 4: Diverse Exploration (Iteration 26+)

Only if stuck:
- Call generate_candidates for non-step families
- Use probe_solution to filter quickly
- Maximum 2 full evals per non-step family

## Evaluation Strategy

1. Generate 10-15 mutations using step_mutator
2. Call probe_solution for all 10-15 (you have 30 probes!)
3. Select top 3-5 by probe score
4. Call evaluate_solution for top 3-5
5. If any beat record: refine that specific mutation type
6. If none beat record: generate new mutation batch

## Constraints

- f(x) ≥ 0: use jnp.maximum(f, 0) or softplus transformation
- Numerical stability: avoid extremely narrow intervals (<2% of domain)
- Start with 600 intervals, refine to 800-1000 if needed
- Keep changes small initially (±5% max)
