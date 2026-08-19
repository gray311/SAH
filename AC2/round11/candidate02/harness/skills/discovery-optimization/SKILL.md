---
name: discovery-optimization
description: "Mathematically-grounded pattern discovery for C\u2082 maximization. Use c2_mutation_engine to get concrete mutation proposals with actual numbers (not symbolic expressions like \"min_h * 0.7\"). Focus on discovering entirely new architectures rather than small parameter tweaks."
---

# C₂ Maximizer: Concrete Mutation Protocol


## Core Principle

The seed program's 13 step patterns are already locally optimized. Small mutations won't help. You need CONCRETE mutation operators that generate actual numbers.


## Phase 1: Get Concrete Mutations (first iteration)

1. Call c2_mutation_engine to get CONCRETE numerical mutation proposals

2. The engine will return actual numbers like: heights=[0.82, 1.97, 0.71, ...], not symbolic expressions

3. Choose ONE mutation proposal that looks promising


## Phase 2: Implement the Mutation

Using the concrete numbers from c2_mutation_engine:

- Rewrite the _create_step_initializer method with the actual numbers
- Target: complex new patterns (3+ levels, asymmetric, varied heights)
- Use SEARCH/REPLACE to update the height values in each pattern variant


## Phase 3: Evaluation Strategy

- Each implemented pattern: call evaluate_solution ONCE (probe is unreliable)

- Track which pattern CLASS improves, not just individual parameters

- If a class works: generate more variants in that class using c2_mutation_engine

- If all fail: call c2_mutation_engine again for new directions


## Phase 4: Iteration

1. Call c2_mutation_engine for concrete numbers → 2. Implement ONE mutation → 3. Evaluate → 4. Drill down or diversify

Key: Work with CONCRETE numbers, not symbolic expressions. The c2_mutation_engine will give you actual height values like 1.47, 2.33, 0.89, etc.
