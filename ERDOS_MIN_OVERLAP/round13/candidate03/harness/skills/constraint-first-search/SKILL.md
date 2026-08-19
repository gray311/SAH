---
name: constraint-first-search
description: Generate functions with EXACT integral=1 before optimizing overlap. Use probes to screen valid candidates.
---

# Constraint-First Search Strategy

## Key Principle
The seed optimizer wastes iterations on constraint fixing. Generate h with ∫h=1 EXACTLY, then optimize overlap.

## Workflow
1. Call normalize_to_integral_one to get 5+ normalized candidates
2. EDIT seed to use ONE normalized candidate as INITIAL h (no sigmoid, no training)
3. Call probe_solution immediately (no training) to get c5_bound estimate
4. Call evaluate_solution on candidates with c5_bound < 0.37
5. If stuck, EDIT to make small adjustments to normalized h (shift/resize one interval)

## Tools
- normalize_to_integral_one: generates h with ∫h=1
- probe_solution: screens candidates (check c5_bound, skip training)
- edit_solution: replace initial_latent with normalized h
