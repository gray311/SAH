---
name: discovery-optimization
description: "Systematic combinatorial search for multi-level step functions. Explores height/width/position space\nmethodically rather than trying to fix function type."
---

# Systematic Combinatorial Search for C₂ Maximization

## Understanding the Problem

You're optimizing C₂ for step functions. The seed program already creates piecewise-constant
functions - don't waste time "fixing" them. Instead, explore the parameter space systematically.

## Search Space

Think of a step function as having:
- Several levels (2-6 regions)
- Each level has: height (0.5-2.5), width (10%-40% of domain), position

The current best uses heights around 1.0-2.0 with multiple levels.

## Strategy: Parameter Space Exploration

### Iteration 1: Baseline with variations
1. Take seed's structure (num_intervals=400, heights ~1.0-2.0)
2. Generate 3-5 variations by tweaking:
   - Center height: ±0.2 (try 1.2, 1.4, 1.6)
   - Width of central region: ±5% (try narrower/wider)
   - Add/remove outer levels
3. Probe all variants
4. Evaluate the best 2

### Iteration 2: If no progress, explore heights
1. Keep central region structure
2. Vary heights systematically:
   - Try lower heights (0.7-1.2)
   - Try higher heights (1.8-2.5)
   - Try asymmetric heights
3. Probe → Evaluate best

### Iteration 3+: Scale the search
1. If 3-level functions plateau, try 4-level or 2-level
2. If symmetric functions plateau, try asymmetric
3. If wide functions plateau, try narrow peaks

## Pattern Variation Recipe

When generating variations, think in terms of:
- height_adjustment: ±0.1 to ±0.3 from base
- width_adjustment: ±5% to ±10% from base
- region_adjustment: shift boundaries by ±5%

Combine 2-3 adjustments per variant for diverse search.

## Verification

Before evaluating:
- Confirm the function still uses piecewise patterns (jnp.piecewise or jnp.where with constants)
- No linear expressions like jnp.linspace

## Budget Discipline

- Max 20 full evaluations
- Use ~15-20 probes per iteration to rank many variants
- Only evaluate the single best candidate from each iteration
- If you've used 10 evals with no progress, restart with a completely different strategy
