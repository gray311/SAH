---
name: discovery-optimization
description: "Systematic pattern modification for C\u2082 maximization. Use pattern_generator to get ready-to-use code templates for new step patterns (add levels, create asymmetry, narrow peaks, smooth transitions). Focus on concrete, incremental changes rather than abstract \"new architectures\"."
---

# C₂ Maximizer: Concrete Pattern Modification Protocol

## Core Principle

Don't try to "discover new architectures" - use pattern_generator to get concrete code templates, then evaluate and refine.

## Phase 1: Get a Code Template

1. Call pattern_generator ONCE with your current best pattern info
2. Extract the code template it returns
3. The template will be ready-to-use code for a new _create_step_initializer method

## Phase 2: Edit and Evaluate

1. Use edit_solution to replace the relevant _create_step_initializer section
2. Call evaluate_solution ONCE to test
3. Record the score

## Phase 3: Refine or Generate Again

- If score > 1.03663: refine by adjusting heights ±0.1, positions ±5%
- If score ≤ 1.03663: call pattern_generator again for a different pattern type

## Pattern Types to Try (in order):

1. **Add a level**: Take a 4-level pattern and add a 5th level with intermediate height
2. **Create asymmetry**: Shift existing pattern to have uneven left/right heights
3. **Narrow peak**: Create a very tall, narrow central peak
4. **Smooth transitions**: Use exponential-like decay instead of hard steps

## Key Rules:

- ONE evaluation per iteration (don't waste probes)
- Small changes: adjust heights by 0.1-0.3, positions by 5%
- Always start with pattern_generator's template
- If stuck, try a completely different pattern type
