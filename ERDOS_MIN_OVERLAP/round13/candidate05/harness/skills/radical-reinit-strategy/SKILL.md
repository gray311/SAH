---
name: radical-reinit-strategy
description: Escape local minima by generating radically different initialization structures. Use probes to screen before evaluation.
---

# Radical Reinitialization Strategy

## Why the Seed Fails
The seed's 12 patterns are all Gaussian/sigmoid-based. They explore similar regions.

## The Fix
Generate INITIALLY DIFFERENT structures that cannot be reached by tuning.

## Pattern Types to Try
- Binary step functions (sharp cutoffs)
- Piecewise constant with 2-4 regions
- Asymmetric distributions
- Multi-peak with narrow support
- Sparse distributions

## Workflow
1. generate_5_init → 5 latents
2. For each: EDIT to use ONLY that latent (num_restarts=1)
3. probe_solution all 5 → screen for c5_bound < 0.37
4. evaluate_solution on best 2
5. If no improvement, repeat with new random seed

## Key Constraints
- integral(h) must be exactly 1
- h(x) in [0,1]
- Use ALL 30 probes before any full evaluation
