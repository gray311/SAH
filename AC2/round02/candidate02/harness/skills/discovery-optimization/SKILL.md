---
name: discovery-optimization
description: "Iteratively optimize a program to maximize C2. Use struct_mutate to generate diverse variants, then probe-based ranking."
---

# C2 Mutation Strategy

## Core Philosophy
The mutator generates diverse variants automatically. Your job is to:
1. Generate mutations with struct_mutate
2. Probe and rank them
3. Evaluate the best
4. Iterate

## When to Use Each Variant Type
- Parameter Perturbations: Use early (evals 0-8)
- Structural Changes: Use mid-search (evals 8-15)
- Representation Switches: Use when stalled

## Budget Allocation
- Total evaluations: 20
