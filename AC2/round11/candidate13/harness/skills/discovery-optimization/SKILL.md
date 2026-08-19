---
name: discovery-optimization
description: "Code-first pattern discovery. Use mutator_tool to generate complete _create_step_initializer methods. Focus on asymmetric, multi-peak, irregular architectures. Refine promising patterns through successive mutations."
---

# C2 Maximization: Direct Code Mutation Protocol

## Core Principle

Do not generate abstract patterns - generate VALID CODE that replaces _create_step_initializer.

## Phase 1: Study the Seed Structure

The seed uses 13 patterns (indices 0-12) with patterns like:
- Pattern 0: Single step, height 1.40, [25%-75%]
- Pattern 3: Multi-level [0.90, 1.90, 0.90] at [15-25%, 25-75%, 75-85%]
- Pattern 4: Three-level [1.10, 2.30, 1.40] with asymmetric intervals

Key observations:
- Heights range from 0.60 to 2.30
- Intervals use percentages like 0.06*n, 0.24*n, 0.44*n
- Patterns are piecewise-constant on the discretized grid

## Phase 2: Generate Mutations

Use mutator_tool to generate COMPLETE pattern implementations:

**Mutation Type A: Increase Peak Height Asymmetry**
- Create patterns with extreme height ratios (e.g., 0.5h to 2.5h)
- This may reduce ||f★f||∞ relative to ||f★f||2^2

**Mutation Type B: Irregular Interval Spacing**
- Use non-uniform percentage breaks (e.g., 0.10, 0.25, 0.50, 0.75, 0.92)
- Avoid the regular 0.20-0.30 gap spacing in seed

**Mutation Type C: Multi-Peak Structures**
- Create 4-6 levels with heights in different proportions
- Example: [0.7h, 1.2h, 2.0h, 1.8h, 1.0h, 0.6h]

**Mutation Type D: Asymmetric Placement**
- Shift the "center of mass" of the pattern
- Do not center all intervals around 50%

## Phase 3: Evaluate and Refine

1. Generate ONE complete _create_step_initializer replacement
2. Call evaluate_solution ONCE (probe is unreliable)
3. If improvement: generate 2-3 variants of the SAME pattern class
4. If no improvement: try a different architectural direction

## Critical Code Rules

- Always use: f = jnp.zeros(n); then f = f.at[...].set(height)
- Percentages must be float multipliers (0.15*n not 0.15*n as int)
- Include all patterns - the executor iterates through all indices
- Heights must be positive floats in [0.3, 3.0]
