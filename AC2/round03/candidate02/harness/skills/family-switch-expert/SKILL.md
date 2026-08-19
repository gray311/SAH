---
name: family-switch-expert
description: Expert playbook for quickly switching between function representation families. Focuses on detecting exhaustion signals and implementing concrete switches to step functions (0.8963 record-holders). Provides code snippets for immediate implementation.
---

# Family Switch Expert Playbook

## Critical Rule

If current C2 < 0.8963 (step function record), you are either:
1. Implementing step functions incorrectly
2. Not implementing step functions at all

## Exhaustion Detection

Call convolution_analyzer after EACH evaluation. It flags exhaustion when:
- Current family hasn't improved in 3+ evals
- Proxy C2 below record-holder for your family
- Same representation class without variant switch

## Immediate Switch Protocol

When exhausted or below 0.8963:

1. STOP current family exploration (max 5 evals/family)
2. CALL convolution_analyzer for code snippet
3. IMPLEMENT the snippet IMMEDIATELY
4. RESUME with probe-based ranking of new family variants

## Step Function Implementation Checklist

When switching to piecewise-constant:
- Use jnp.zeros(N) as base
- Define clear start/end indices
- Set heights with f.at[...].set(value)
- Add tails if needed (0.2-0.5 range)
- Ensure non-negativity
- Test with convolution_analyzer first

## Family Priority

1. STEP FUNCTIONS (0.8963) - Primary target
2. Multi-level step functions
3. Piecewise-linear (only if steps fail)
4. Gaussian mixtures
5. B-splines
6. Exponential combinations

## Probing Discipline

For ANY new family: 8+ probe calls BEFORE 1 full eval
Rank top 3 by probe score
Evaluate only top 3

## When to Finish

- Eval budget exhausted
- Step functions implementation verified (>=0.8963)
- Multiple families exhausted with no path to improvement
