---
name: perturbation-protocol
description: Systematically perturb seed step functions to explore local landscape. Track which perturbations improve C2.
---

# Perturbation Protocol for C2 Maximization

## Core Principle
The seed's step functions are carefully tuned. Don't abandon them.
Systematically perturb heights, widths, and positions to explore local landscape.

## When to Perturb (trigger conditions)
1. At start of each iteration (use structural_mutator to get 8 variants)
2. When probe scores show consistent direction (e.g., height increases always help)
3. When stuck at same score for 3+ iterations

## Perturbation Types
1. Height perturbations: +/-0.1 on peak values
   - If increasing middle peak improved C2, try higher in next iteration
   - If decreasing side peaks helped, apply to similar positions

2. Width perturbations: +/-0.05 fraction of current width
   - Wider peaks might improve L2 norm
   - Narrower peaks might reduce ||f*f||_inf

3. Position perturbations: +/-0.03 fraction of domain
   - Shift peaks to better align with convolution structure
   - Asymmetric shifts might create better interference patterns

## Execution Flow
1. Call structural_mutator on current best to get 8 variants
2. Probe ALL 8 (8 probes per iteration)
3. Evaluate top 2 by probe score
4. Track which perturbations improved score
5. Next iteration: apply successful perturbations, discard failed ones

## Key Rule
NEVER random perturbations. Track which directions work and repeat them.
If all 8 variants fail to improve after 3 iterations: jump to new architecture family.
