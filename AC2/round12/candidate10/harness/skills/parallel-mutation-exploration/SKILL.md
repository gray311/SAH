---
name: parallel-mutation-exploration
description: Parallel exploration of diverse mutation types. Try multiple strategies simultaneously rather than sequentially.
---

# Parallel Mutation Exploration for C₂ Maximization

## Core Strategy

Don't explore mutation types SEQUENTIALLY - explore them PARALLEL. The bottleneck is getting stuck in local optima.

## Iteration Protocol

1. Get 5 mutation proposals from mutation_generator (ensure diversity across types)

2. Pick TOP 2-3 mutations from DIFFERENT types (e.g., one height perturbation, one width expansion, one asymmetric)

3. Implement ALL 2-3 in parallel with edit_solution

4. Evaluate ALL 2-3 with evaluate_solution

5. Keep the BEST result, discard the rest

6. If NO improvement after trying 3+ mutations: call arch_explorer

## When to Use arch_explorer

- 5+ consecutive iterations with no improvement
- Tried 4+ different mutation types without success
- Current pattern has been refined for 10+ iterations with diminishing returns

## Key Insight

Parallel exploration prevents premature convergence. Sequential exploration gets you stuck.

Always try MULTIPLE diverse approaches before concluding a strategy is exhausted.
