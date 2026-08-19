---
name: discovery-optimization
description: "Discover functions maximizing C\u2082 = ||f\u2605f||\u2082\u00b2 / (||f\u2605f||\u2081 ||f\u2605f||_\u221e). Use bounded internal search inside function constructors. Explore splines, learned mixtures, and hybrid step+smooth constructions. Use probe_solution to rank families before full evaluation."
---

# C₂ Maximization Strategy

## Objective
Maximize C₂ = ||f★f||₂² / (||f★f||₁ ||f★f||_∞) where f: R→R, f≥0.
Benchmark: 0.89628. Seed achieves ~0.926.

## Core Principle: EXPLORE NEW FUNCTION FAMILIES
The seed uses fixed multi-level step functions. To beat it, you MUST:
1. Rewrite the function CONSTRUCTION entirely (not just hyperparameters)
2. Try SPLINES (B-splines with optimized knots)
3. Try LEARNED MIXTURES (weighted combinations of basis functions)
4. Try HYBRID step+smooth (step with smooth transitions)

## Method: Bounded Internal Search
Inside your function constructor, do a SMALL bounded search (5-10 configs):
- For splines: try different knot placements, basis weights
- For mixtures: try different component weights, number of components
- For hybrids: try different step widths, transition smoothness

Pick the best config and use it in the program.

## Tool Usage
1. WRITE THE NEW FUNCTION CONSTRUCTION (full rewrite of the EVOLVE-BLOCK's function part)
2. CALL probe_solution to quickly rank your construction (use subsampled data)
3. If probe succeeds and score looks promising, CALL evaluate_solution
4. Iterate on the CONSTRUCTION, not parameters

## Don'ts
- NEVER just change hyperparameters (learning_rate, num_steps, etc.)
- NEVER try 20+ internal search configs (too slow)
- NEVER use the same function construction twice
