---
name: c2-mutation-strategy
description: A method playbook for using struct_mutate to escape local optima.
---

# C2 Mutation Strategy Guide

## Core Philosophy
1. Generate mutations with struct_mutate
2. Probe and rank them
3. Evaluate the best
4. Iterate

## When to Use
- Parameter Perturbations: Early (evals 0-8)
- Structural Changes: Mid-search (evals 8-15)
- Representation Switches: When stalled

## Workflow
1. Call struct_mutate to get 3-5 variants
2. Call probe_solution on each (3-5 probes total)
3. Call evaluate_solution on best variant
4. If improvement: generate new mutations
5. If no improvement: try representation switch

## Budget
- Total evaluations: 20
- Use probes aggressively
