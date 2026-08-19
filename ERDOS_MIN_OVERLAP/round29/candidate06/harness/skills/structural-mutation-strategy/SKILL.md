---
name: structural-mutation-strategy
description: Prioritize structural mutations over hyperparameter tuning. Generate diverse step functions by transforming existing ones.
---

# Structural Mutation Strategy for Erdos C5

## Core Principle
The optimizer's initial configurations and hyperparameters are likely near a local optimum.
STRUCTURAL CHANGES to h (shift, split, merge, add/remove peaks) can escape this optimum.

## Workflow

1. START: Get the current best h (from seed or previous iterations)

2. MUTATE: Call mutate_h_structure with different mutation types:
   - shift: Move the entire function left/right
   - split: Divide wide peaks into narrower ones
   - add_peak: Insert a new peak
   - remove_peak: Eliminate a suboptimal peak

3. SCREEN: Use probe_solution on each mutated h (cheap, ~10s each)

4. EVALUATE: Call evaluate_solution on the BEST 2 candidates (lowest c5_bound)

5. ITERATE: If no improvement, repeat with different mutation types

6. LAST RESORT: Only after 2 failed structural searches, tune hyperparameters

## Why This Works
- Structural changes can escape local optima that hyperparameter tuning cannot
- The C5 objective is non-convex; different peak arrangements yield very different results
- The seed optimizer's 15 patterns are limited; structural mutation generates truly new configurations
