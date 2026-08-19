---
name: step-pattern-optimization
description: Optimize step functions by exploring level counts, heights, and asymmetries. Use probes to rapidly test 10+ variants. Smooth functions fail - stay with steps.
---

# Step Pattern Optimization Protocol

## Core Principle
Step functions maximize C2 by creating sharp convolution peaks. Smooth functions UNDERPERFORM.

## When to Generate New Patterns (trigger conditions)
1. At start of search (iteration 0)
2. After 3 failed evaluations on same pattern family
3. After iteration 10 without improvement
4. When probe scores plateau across 5+ variants

## Pattern Engineering Checklist
1. **Level count**: Try 4-12 levels (more granularity than seed's 2-5)
2. **Height range**: Use heights from 0.3 to 3.0 (extreme values)
3. **Asymmetry**: Test symmetric (pyramid) vs asymmetric (shifted)
4. **Support width**: Narrow (50%) vs wide (80%) vs full (100%)
5. **Shape**: Pyramid, mountain, staircase, dual-peak, flat-top

## Execution Flow
1. Call generate_step_patterns to get 7 diverse patterns
2. Implement ONE pattern in EVOLVE-BLOCK (use jnp.at for efficiency)
3. Call probe_solution to get approximate score
4. If probe < 1.0: try next pattern (don't waste full eval)
5. If probe >= 1.0: call evaluate_solution on top 2 patterns
6. If one beats record: switch to Phase 2 (refinement). Otherwise: generate MORE patterns

## Key Rules
- STICK TO STEP FUNCTIONS - they are proven to beat smooth functions
- Use 30 probes to explore 15-25 step patterns before full evaluations
- NEVER try Gaussian/B-spline/oscillatory - they smooth convolution peaks
